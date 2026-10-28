"""Artifact contracts. The PRD is complete. Later artifacts are typed stubs."""

from dataclasses import dataclass

from factory.errors import ContractError


@dataclass(frozen=True)
class PRD:
    """Product requirements the product agent must fill before PRD review."""

    problem: str
    users: str
    scope: str
    out_of_scope: str
    acceptance_criteria: tuple[str, ...]
    open_questions: tuple[str, ...]


@dataclass(frozen=True)
class DesignArtifact:
    """Typed stub. No generator in this build."""

    user_flows: tuple[str, ...] = ()
    interfaces: tuple[str, ...] = ()


@dataclass(frozen=True)
class ArchitectureArtifact:
    """Typed stub. No generator in this build.

    `dependency_graph` holds directed edges of (dependent, dependency).
    """

    components: tuple[str, ...] = ()
    boundaries: tuple[str, ...] = ()
    dependency_graph: tuple[tuple[str, str], ...] = ()


@dataclass(frozen=True)
class PRReviewPacket:
    """Typed stub. No generator in this build."""

    matches: tuple[str, ...] = ()
    mismatches: tuple[str, ...] = ()
    pr_link: str = ""


def validate_prd(prd: PRD) -> None:
    """Reject a PRD that leaves a required field blank."""
    errors: list[str] = []
    for name in ("problem", "users", "scope", "out_of_scope"):
        value = getattr(prd, name)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{name} is required")
    criteria = prd.acceptance_criteria
    if not isinstance(criteria, (list, tuple)) or len(criteria) == 0:
        errors.append("acceptance_criteria is required")
    elif any(not isinstance(item, str) or not item.strip() for item in criteria):
        errors.append("acceptance_criteria items must be non-empty strings")
    questions = prd.open_questions
    if not isinstance(questions, (list, tuple)):
        errors.append("open_questions must be a list")
    elif any(not isinstance(item, str) or not item.strip() for item in questions):
        errors.append("open_questions items must be non-empty strings")
    if errors:
        raise ContractError(errors)


def render_prd(prd: PRD) -> str:
    """Render a validated PRD as the Jira comment body."""
    lines = [
        "## PRD",
        "",
        "### Problem",
        prd.problem.strip(),
        "",
        "### Users",
        prd.users.strip(),
        "",
        "### Scope",
        prd.scope.strip(),
        "",
        "### Out of scope",
        prd.out_of_scope.strip(),
        "",
        "### Acceptance criteria",
    ]
    for item in prd.acceptance_criteria:
        lines.append(f"- {item.strip()}")
    lines.extend(["", "### Open questions"])
    if prd.open_questions:
        for item in prd.open_questions:
            lines.append(f"- {item.strip()}")
    else:
        lines.append("None.")
    return "\n".join(lines) + "\n"
