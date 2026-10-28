"""Jira adapter: in-memory behavior and the REST client with a fake transport."""

import io
import json
import urllib.error
import urllib.request

import pytest

from factory.config import load_settings
from factory.errors import ConfigError, JiraError
from factory.jira import InMemoryJira, MutableTicket, RestJira, _plain_text
from factory.stages import Stage


def test_in_memory_replaces_only_the_stage_label():
    stored = MutableTicket(
        key="PROJ-1",
        summary="S",
        description="D",
        labels=["bug", "prd_draft"],
        project_key="PROJ",
    )
    jira = InMemoryJira({"PROJ-1": stored}, project_key="PROJ")
    jira.post_comment("PROJ-1", "hello")
    jira.set_stage("PROJ-1", Stage.PRD_REVIEW)
    ticket = jira.get_ticket("PROJ-1")
    assert ticket.comments == ("hello",)
    assert ticket.labels == ("bug", "prd_review")
    assert ticket.stage is Stage.PRD_REVIEW


def test_in_memory_rejects_a_different_project():
    stored = MutableTicket(key="OTHER-1", summary="S", project_key="OTHER")
    jira = InMemoryJira({"OTHER-1": stored}, project_key="PROJ")
    with pytest.raises(JiraError, match="not PROJ"):
        jira.get_ticket("OTHER-1")


def test_settings_come_from_the_environment_and_keep_default_labels():
    settings = load_settings(
        {
            "JIRA_BASE_URL": "https://example.atlassian.net/",
            "JIRA_EMAIL": "dev@example.com",
            "JIRA_API_TOKEN": "not-a-real-token",
            "JIRA_PROJECT_KEY": "PROJ",
            "FACTORY_STAGE_LABELS": '{"prd_review": "sf-prd-review"}',
        }
    )
    assert settings.jira_base_url == "https://example.atlassian.net"
    assert settings.stage_labels[Stage.PRD_DRAFT] == "prd_draft"
    assert settings.stage_labels[Stage.PRD_REVIEW] == "sf-prd-review"
    with pytest.raises(ConfigError, match="Missing environment"):
        load_settings({})


class _FakeResponse:
    def __init__(self, payload: dict):
        self._raw = json.dumps(payload).encode("utf-8")

    def read(self) -> bytes:
        return self._raw

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False


def test_rest_adapter_reads_posts_and_sets_the_stage_label(monkeypatch):
    calls = []
    issue = {
        "key": "PROJ-1",
        "fields": {
            "summary": "Export failures",
            "description": "Rows drop.",
            "labels": ["bug", "prd_draft"],
            "project": {"key": "PROJ"},
            "comment": {"comments": [{"body": "earlier note"}]},
        },
    }

    def fake_urlopen(request, timeout=30):
        calls.append(request)
        assert timeout == 30
        if request.method == "GET":
            return _FakeResponse(issue)
        if request.method == "PUT":
            body = json.loads(request.data.decode("utf-8"))
            issue["fields"]["labels"] = ["bug", "prd_review"]
            assert body == {
                "update": {
                    "labels": [
                        {"remove": "prd_draft"},
                        {"add": "prd_review"},
                    ]
                }
            }
            return _FakeResponse({})
        posted = json.loads(request.data.decode("utf-8"))
        assert posted == {"body": "hello"}
        return _FakeResponse({})

    monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)
    jira = RestJira(
        base_url="https://example.atlassian.net",
        email="dev@example.com",
        api_token="not-a-real-token",
        project_key="PROJ",
    )
    ticket = jira.get_ticket("PROJ-1")
    assert ticket.summary == "Export failures"
    assert ticket.stage is Stage.PRD_DRAFT
    assert ticket.comments == ("earlier note",)
    jira.post_comment("PROJ-1", "hello")
    jira.set_stage("PROJ-1", Stage.PRD_REVIEW)
    assert [call.get_method() for call in calls] == ["GET", "POST", "GET", "PUT"]
    assert calls[0].full_url.endswith(
        "/rest/api/2/issue/PROJ-1?fields=summary,description,labels,project,comment"
    )
    auth = calls[0].get_header("Authorization")
    assert auth.startswith("Basic ")
    assert "not-a-real-token" not in auth


def test_rest_error_does_not_echo_the_token(monkeypatch):
    def fake_urlopen(request, timeout=30):
        raise urllib.error.HTTPError(
            request.full_url,
            401,
            "Unauthorized",
            hdrs=None,
            fp=io.BytesIO(b"nope"),
        )

    monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)
    jira = RestJira(
        base_url="https://example.atlassian.net",
        email="dev@example.com",
        api_token="super-secret-token",
        project_key="PROJ",
    )
    with pytest.raises(JiraError) as caught:
        jira.get_ticket("PROJ-1")
    assert "super-secret-token" not in str(caught.value)
    assert "HTTP 401" in str(caught.value)


def test_plain_text_flattens_an_atlassian_document():
    value = {
        "type": "doc",
        "content": [
            {
                "type": "paragraph",
                "content": [{"type": "text", "text": "Rows drop."}],
            }
        ],
    }
    assert _plain_text(value) == "Rows drop."
    assert _plain_text(None) == ""
