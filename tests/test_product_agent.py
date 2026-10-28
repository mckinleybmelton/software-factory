"""Product agent drafts a PRD from ticket fields and does not call a model."""

from factory.context import TicketSlice
from factory.contracts import validate_prd
from factory.product import ProductAgent
from factory.stages import Stage


def _slice(summary: str, description: str, key: str = "PROJ-1") -> TicketSlice:
    return TicketSlice(key=key, summary=summary, description=description, stage=Stage.PRD_DRAFT)


def test_summary_and_description_map_into_the_problem():
    prd = ProductAgent().draft(_slice("Export failures", "The nightly job drops rows."))
    assert prd.problem == "From the ticket:\nExport failures\n\nThe nightly job drops rows."
    validate_prd(prd)


def test_missing_sections_are_unanswered_placeholders():
    prd = ProductAgent().draft(_slice("Export failures", "The nightly job drops rows."))
    assert prd.users == "Unanswered. The ticket does not state users."
    assert prd.scope == "Unanswered. The ticket does not state scope."
    assert prd.out_of_scope == "Unanswered. The ticket does not state out of scope."
    assert prd.acceptance_criteria == (
        "Unanswered. The ticket does not state acceptance criteria.",
    )
    assert "Who are the users?" in prd.open_questions
    assert "What is in scope?" in prd.open_questions
    assert "What is out of scope?" in prd.open_questions
    assert "What are the acceptance criteria?" in prd.open_questions
    assert not any(question.startswith("From the ticket:") for question in prd.open_questions)


def test_labeled_sections_come_from_the_ticket():
    description = "\n".join(
        [
            "Users: warehouse leads",
            "Scope: nightly CSV export",
            "Out of scope: PDF reports",
            "Acceptance criteria:",
            "- File lands in the bucket",
            "- Header row is present",
            "Open questions:",
            "- Which timezone?",
        ]
    )
    prd = ProductAgent().draft(_slice("Export failures", description))
    assert prd.users == "From the ticket: warehouse leads"
    assert prd.scope == "From the ticket: nightly CSV export"
    assert prd.out_of_scope == "From the ticket: PDF reports"
    assert prd.acceptance_criteria == (
        "From the ticket: File lands in the bucket",
        "From the ticket: Header row is present",
    )
    assert prd.open_questions == ("From the ticket: Which timezone?",)
    assert "Unanswered" not in prd.users
    assert "Unanswered" not in prd.scope
    validate_prd(prd)


def test_markdown_headings_are_read_as_sections():
    description = "\n".join(
        [
            "## Users",
            "billing admins",
            "## Scope",
            "invoice export",
        ]
    )
    prd = ProductAgent().draft(_slice("Invoices", description))
    assert prd.users == "From the ticket: billing admins"
    assert prd.scope == "From the ticket: invoice export"
    assert prd.out_of_scope.startswith("Unanswered.")
    assert "What is out of scope?" in prd.open_questions
    assert "Who are the users?" not in prd.open_questions


def test_empty_ticket_leaves_the_problem_unanswered():
    prd = ProductAgent().draft(_slice("", "  "))
    assert prd.problem == "Unanswered. The ticket does not state the problem."
    assert "What problem should this PRD solve?" in prd.open_questions
    validate_prd(prd)


def test_agent_stops_at_prd_review():
    assert ProductAgent.STOP_STAGE is Stage.PRD_REVIEW
