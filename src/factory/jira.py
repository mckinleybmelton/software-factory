"""Jira adapter. The only writer to Jira.

`RestJira` talks to the Jira REST API v2 with basic auth (email + API token).
`InMemoryJira` is the fake used by tests. It does not touch the network.
"""

import base64
import json
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from typing import Protocol
from urllib.parse import quote

from factory.config import Settings, default_stage_labels
from factory.errors import JiraError
from factory.stages import Stage, stage_from_labels


@dataclass(frozen=True)
class Ticket:
    """Snapshot returned by the adapter. Comments stay here, not in agent context."""

    key: str
    summary: str
    description: str
    stage: Stage
    labels: tuple[str, ...]
    comments: tuple[str, ...]
    project_key: str


@dataclass
class MutableTicket:
    """Stored ticket for the in-memory adapter."""

    key: str
    summary: str
    description: str = ""
    labels: list[str] = field(default_factory=list)
    comments: list[str] = field(default_factory=list)
    project_key: str = ""


class JiraClient(Protocol):
    def get_ticket(self, key: str) -> Ticket:
        """Read one ticket by key."""

    def post_comment(self, key: str, body: str) -> None:
        """Append a comment. Artifacts and gate notes both use this."""

    def set_stage(self, key: str, stage: Stage) -> None:
        """Replace the stage label, leaving every other label in place."""


class InMemoryJira:
    """Fake Jira. Tests construct this directly so nothing is sent over the network."""

    def __init__(
        self,
        tickets: dict[str, MutableTicket],
        *,
        project_key: str,
        stage_labels: dict[Stage, str] | None = None,
    ):
        self._tickets = tickets
        self._project_key = project_key
        self._stage_labels = stage_labels or default_stage_labels()

    def get_ticket(self, key: str) -> Ticket:
        stored = self._require(key)
        self._check_project(stored.key, stored.project_key)
        return Ticket(
            key=stored.key,
            summary=stored.summary,
            description=stored.description,
            stage=stage_from_labels(stored.labels, self._stage_labels),
            labels=tuple(stored.labels),
            comments=tuple(stored.comments),
            project_key=stored.project_key,
        )

    def post_comment(self, key: str, body: str) -> None:
        stored = self._require(key)
        self._check_project(stored.key, stored.project_key)
        stored.comments.append(body)

    def set_stage(self, key: str, stage: Stage) -> None:
        stored = self._require(key)
        self._check_project(stored.key, stored.project_key)
        stage_values = set(self._stage_labels.values())
        stored.labels = [label for label in stored.labels if label not in stage_values]
        stored.labels.append(self._stage_labels[stage])

    def _require(self, key: str) -> MutableTicket:
        stored = self._tickets.get(key)
        if stored is None:
            raise JiraError(f"Ticket {key} was not found.")
        return stored

    def _check_project(self, key: str, project_key: str) -> None:
        if project_key != self._project_key:
            raise JiraError(
                f"Ticket {key} is in project {project_key or '(unknown)'}, "
                f"not {self._project_key}."
            )


class RestJira:
    """Jira Cloud or Server REST API v2. Comment bodies are plain text."""

    def __init__(
        self,
        *,
        base_url: str,
        email: str,
        api_token: str,
        project_key: str,
        stage_labels: dict[Stage, str] | None = None,
        opener: urllib.request.OpenerDirector | None = None,
    ):
        self._base_url = base_url.rstrip("/")
        self._email = email
        self._api_token = api_token
        self._project_key = project_key
        self._stage_labels = stage_labels or default_stage_labels()
        self._opener = opener

    @classmethod
    def from_settings(cls, settings: Settings) -> "RestJira":
        return cls(
            base_url=settings.jira_base_url,
            email=settings.jira_email,
            api_token=settings.jira_api_token,
            project_key=settings.jira_project_key,
            stage_labels=settings.stage_labels,
        )

    def get_ticket(self, key: str) -> Ticket:
        path = _issue_path(key) + "?fields=summary,description,labels,project,comment"
        payload = self._request("GET", path)
        return self._ticket_from_payload(key, payload)

    def post_comment(self, key: str, body: str) -> None:
        self._request("POST", _issue_path(key) + "/comment", {"body": body})

    def set_stage(self, key: str, stage: Stage) -> None:
        ticket = self.get_ticket(key)
        stage_values = set(self._stage_labels.values())
        ops = [{"remove": label} for label in ticket.labels if label in stage_values]
        ops.append({"add": self._stage_labels[stage]})
        self._request("PUT", _issue_path(key), {"update": {"labels": ops}})

    def _ticket_from_payload(self, key: str, payload: dict) -> Ticket:
        fields = payload.get("fields") or {}
        project_key = str((fields.get("project") or {}).get("key") or "")
        if project_key != self._project_key:
            raise JiraError(
                f"Ticket {key} is in project {project_key or '(unknown)'}, "
                f"not {self._project_key}."
            )
        labels = tuple(str(label) for label in (fields.get("labels") or []))
        comment_field = fields.get("comment") or {}
        comments = tuple(
            _plain_text(comment.get("body"))
            for comment in (comment_field.get("comments") or [])
        )
        return Ticket(
            key=str(payload.get("key") or key),
            summary=_plain_text(fields.get("summary")),
            description=_plain_text(fields.get("description")),
            stage=stage_from_labels(labels, self._stage_labels),
            labels=labels,
            comments=comments,
            project_key=project_key,
        )

    def _request(self, method: str, path: str, payload: dict | None = None) -> dict:
        url = self._base_url + path
        data = None
        headers = {
            "Authorization": "Basic " + _basic_token(self._email, self._api_token),
            "Accept": "application/json",
        }
        if payload is not None:
            data = json.dumps(payload).encode("utf-8")
            headers["Content-Type"] = "application/json"
        request = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            if self._opener is not None:
                response_cm = self._opener.open(request, timeout=30)
            else:
                response_cm = urllib.request.urlopen(request, timeout=30)
            with response_cm as response:
                raw = response.read()
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")[:500]
            raise JiraError(
                f"Jira {method} {path} failed with HTTP {exc.code}: {detail}"
            ) from exc
        except urllib.error.URLError as exc:
            raise JiraError(f"Jira {method} {path} failed: {exc.reason}") from exc
        if not raw:
            return {}
        parsed = json.loads(raw.decode("utf-8"))
        if not isinstance(parsed, dict):
            raise JiraError(f"Jira {method} {path} returned a non-object response.")
        return parsed


def _issue_path(key: str) -> str:
    return "/rest/api/2/issue/" + quote(key, safe="-")


def _basic_token(email: str, api_token: str) -> str:
    raw = f"{email}:{api_token}".encode("utf-8")
    return base64.b64encode(raw).decode("ascii")


def _plain_text(value: object) -> str:
    """Accept a Jira string or a v3-style document tree."""
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    texts: list[str] = []

    def walk(node: object) -> None:
        if isinstance(node, dict):
            if node.get("type") == "text" and isinstance(node.get("text"), str):
                texts.append(node["text"])
            content = node.get("content")
            if isinstance(content, list):
                for child in content:
                    walk(child)
        elif isinstance(node, list):
            for child in node:
                walk(child)

    walk(value)
    return "\n".join(texts)
