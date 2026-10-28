"""Product agent. Drafts a PRD from the ticket and stops at PRD review.

There is no live model call. Labeled sections in the ticket are copied through.
Anything the ticket does not state becomes an explicit unanswered placeholder.
"""

import re

from factory.context import TicketSlice
from factory.contracts import PRD
from factory.stages import Stage

# Longer labels first so "out of scope" is not read as "scope".
_LABELS: tuple[tuple[str, str], ...] = (
    ("out of scope", "out_of_scope"),
    ("out-of-scope", "out_of_scope"),
    ("acceptance criteria", "acceptance"),
    ("acceptance criterion", "acceptance"),
    ("open questions", "open_questions"),
    ("open question", "open_questions"),
    ("users", "users"),
    ("user", "users"),
    ("scope", "scope"),
)

_GAP_QUESTIONS: tuple[tuple[str, str], ...] = (
    ("users", "Who are the users?"),
    ("scope", "What is in scope?"),
    ("out_of_scope", "What is out of scope?"),
    ("acceptance", "What are the acceptance criteria?"),
)

_BULLET = re.compile(r"^(?:[-*]|\d+[.)])\s+(.*)$")


class ProductAgent:
    """Drafts the PRD. The orchestrator posts it and moves the stage."""

    STOP_STAGE = Stage.PRD_REVIEW

    def draft(self, context: TicketSlice) -> PRD:
        sections = _sections(context.summary, context.description)
        questions: list[str] = []

        problem = _problem(context.summary, context.description)
        if problem.startswith("Unanswered."):
            questions.append("What problem should this PRD solve?")

        users, users_known = _field(sections.get("users"), "users")
        scope, scope_known = _field(sections.get("scope"), "scope")
        out_of_scope, out_known = _field(sections.get("out_of_scope"), "out of scope")
        acceptance, acceptance_known = _acceptance(sections.get("acceptance"))

        for item in _items(sections.get("open_questions", "")):
            questions.append(f"From the ticket: {item}")

        known = {
            "users": users_known,
            "scope": scope_known,
            "out_of_scope": out_known,
            "acceptance": acceptance_known,
        }
        for key, question in _GAP_QUESTIONS:
            if not known[key]:
                questions.append(question)

        return PRD(
            problem=problem,
            users=users,
            scope=scope,
            out_of_scope=out_of_scope,
            acceptance_criteria=tuple(acceptance),
            open_questions=tuple(questions),
        )


def _problem(summary: str, description: str) -> str:
    parts = [part.strip() for part in (summary, description) if part and part.strip()]
    if not parts:
        return "Unanswered. The ticket does not state the problem."
    return "From the ticket:\n" + "\n\n".join(parts)


def _field(section: str | None, name: str) -> tuple[str, bool]:
    if section and section.strip():
        return f"From the ticket: {section.strip()}", True
    return f"Unanswered. The ticket does not state {name}.", False


def _acceptance(section: str | None) -> tuple[list[str], bool]:
    items = _items(section or "")
    if items:
        return [f"From the ticket: {item}" for item in items], True
    return ["Unanswered. The ticket does not state acceptance criteria."], False


def _items(block: str) -> list[str]:
    bullets = []
    for line in block.splitlines():
        match = _BULLET.match(line.strip())
        if match and match.group(1).strip():
            bullets.append(match.group(1).strip())
    if bullets:
        return bullets
    text = block.strip()
    return [text] if text else []


def _sections(summary: str, description: str) -> dict[str, str]:
    """Pull labeled sections from the summary and the description.

    Description wins when both name the same section, because that is where
    the ticket body states the requirement.
    """
    found = _parse_sections(summary)
    for key, value in _parse_sections(description).items():
        if value or key not in found:
            found[key] = value
    return found


def _parse_sections(text: str) -> dict[str, str]:
    sections: dict[str, list[str]] = {}
    current: str | None = None
    for line in text.splitlines():
        header = _header(line)
        if header is not None:
            current, rest = header
            bucket = sections.setdefault(current, [])
            if rest:
                bucket.append(rest)
            continue
        if current is not None:
            sections.setdefault(current, []).append(line)
    return {key: "\n".join(lines).strip() for key, lines in sections.items()}


def _header(line: str) -> tuple[str, str] | None:
    text = re.sub(r"^#{1,6}\s+", "", line.strip())
    lowered = text.lower()
    for label, key in _LABELS:
        if lowered == label:
            return key, ""
        prefix = label + ":"
        if lowered.startswith(prefix):
            return key, text[len(prefix) :].strip()
    return None
