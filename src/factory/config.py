"""Environment configuration. Secrets stay in the environment, never in the repo."""

import json
import os
from dataclasses import dataclass
from typing import Mapping

from factory.errors import ConfigError
from factory.stages import Stage

JIRA_BASE_URL = "JIRA_BASE_URL"
JIRA_EMAIL = "JIRA_EMAIL"
JIRA_API_TOKEN = "JIRA_API_TOKEN"
JIRA_PROJECT_KEY = "JIRA_PROJECT_KEY"
STAGE_LABELS_ENV = "FACTORY_STAGE_LABELS"

REQUIRED_ENV = (JIRA_BASE_URL, JIRA_EMAIL, JIRA_API_TOKEN, JIRA_PROJECT_KEY)


@dataclass(frozen=True)
class Settings:
    jira_base_url: str
    jira_email: str
    jira_api_token: str
    jira_project_key: str
    stage_labels: dict[Stage, str]


def default_stage_labels() -> dict[Stage, str]:
    """Label text equals the stage name unless config overrides it."""
    return {stage: stage.value for stage in Stage}


def resolve_stage_labels(override: Mapping[str, str] | None = None) -> dict[Stage, str]:
    """Merge a partial stage-to-label map over the defaults."""
    labels = default_stage_labels()
    if not override:
        return labels
    known = {stage.value: stage for stage in Stage}
    unknown = sorted(set(override) - set(known))
    if unknown:
        raise ConfigError("Unknown stage in label map: " + ", ".join(unknown))
    for name, label in override.items():
        if not isinstance(label, str) or not label.strip():
            raise ConfigError(f"Label for {name} must be a non-empty string.")
        labels[known[name]] = label.strip()
    seen: dict[str, Stage] = {}
    for stage, label in labels.items():
        other = seen.get(label)
        if other is not None:
            raise ConfigError(
                f"Stage label {label!r} is used for both {other.value} and {stage.value}."
            )
        seen[label] = stage
    return labels


def load_settings(env: Mapping[str, str] | None = None) -> Settings:
    """Read Jira credentials and the optional stage-label map from the environment."""
    source = os.environ if env is None else env
    missing = [name for name in REQUIRED_ENV if not source.get(name, "").strip()]
    if missing:
        raise ConfigError(
            "Missing environment variables: "
            + ", ".join(missing)
            + ". Set JIRA_BASE_URL, JIRA_EMAIL, JIRA_API_TOKEN, and JIRA_PROJECT_KEY."
        )
    raw_labels = source.get(STAGE_LABELS_ENV, "").strip()
    override: dict[str, str] | None = None
    if raw_labels:
        try:
            parsed = json.loads(raw_labels)
        except json.JSONDecodeError as exc:
            raise ConfigError(f"{STAGE_LABELS_ENV} must be a JSON object.") from exc
        if not isinstance(parsed, dict):
            raise ConfigError(f"{STAGE_LABELS_ENV} must be a JSON object.")
        override = parsed
    return Settings(
        jira_base_url=source[JIRA_BASE_URL].strip().rstrip("/"),
        jira_email=source[JIRA_EMAIL].strip(),
        jira_api_token=source[JIRA_API_TOKEN].strip(),
        jira_project_key=source[JIRA_PROJECT_KEY].strip(),
        stage_labels=resolve_stage_labels(override),
    )
