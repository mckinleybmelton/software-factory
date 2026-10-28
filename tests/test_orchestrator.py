"""Orchestrator run and resume against the in-memory Jira adapter."""

from dataclasses import fields

import pytest

from factory.cli import main
from factory.context import TicketSlice
from factory.contracts import PRD
from factory.errors import ContractError, OrchestratorError
from factory.jira import InMemoryJira, MutableTicket
from factory.orchestrator import Orchestrator
from factory.product import ProductAgent
from factory.stages import Stage


class SpyProduct(ProductAgent):
    def __init__(self):
        self.contexts: list[TicketSlice] = []

    def draft(self, context: TicketSlice) -> PRD:
        self.contexts.append(context)
        return super().draft(context)


def _stack(labels: list[str] | None = None, comments: list[str] | None = None):
    stored = MutableTicket(
        key="PROJ-1",
        summary="Export failures",
        description="The nightly job drops rows.",
        labels=list(labels or []),
        comments=list(comments or []),
        project_key="PROJ",
    )
    jira = InMemoryJira({"PROJ-1": stored}, project_key="PROJ")
    spy = SpyProduct()
    return Orchestrator(jira, spy), jira, spy


def test_run_posts_the_prd_and_sets_prd_review():
    orch, jira, spy = _stack()
    result = orch.run("PROJ-1")
    ticket = jira.get_ticket("PROJ-1")
    assert result.stage is Stage.PRD_REVIEW
    assert ticket.stage is Stage.PRD_REVIEW
    assert ticket.labels == ("prd_review",)
    assert len(ticket.comments) == 1
    body = ticket.comments[0]
    assert body.startswith("## PRD")
    assert "From the ticket:\nExport failures" in body
    assert "The nightly job drops rows." in body
    assert "agent: product" in body
    assert "stage: prd_draft -> prd_review" in body
    assert "version: 1" in body
    assert spy.contexts[0].key == "PROJ-1"
    assert spy.contexts[0].stage is Stage.PRD_DRAFT


def test_missing_stage_is_treated_as_prd_draft():
    orch, jira, _spy = _stack(labels=["bug"])
    orch.run("PROJ-1")
    ticket = jira.get_ticket("PROJ-1")
    assert ticket.stage is Stage.PRD_REVIEW
    assert "bug" in ticket.labels
    assert "prd_review" in ticket.labels
    assert "prd_draft" not in ticket.labels


def test_run_refuses_every_stage_except_prd_draft():
    orch, jira, spy = _stack(labels=["design_draft"])
    with pytest.raises(OrchestratorError, match="only runs the product agent"):
        orch.run("PROJ-1")
    ticket = jira.get_ticket("PROJ-1")
    assert ticket.comments == ()
    assert ticket.stage is Stage.DESIGN_DRAFT
    assert spy.contexts == []


def test_product_context_excludes_other_transcripts():
    orch, jira, spy = _stack(
        comments=["Reviewer transcript: do not show this to the product agent."]
    )
    orch.run("PROJ-1")
    context = spy.contexts[0]
    assert [field.name for field in fields(context)] == [
        "key",
        "summary",
        "description",
        "stage",
    ]
    assert not hasattr(context, "comments")
    posted = jira.get_ticket("PROJ-1").comments[-1]
    assert "Reviewer transcript" not in posted
    assert "version: 1" in posted


def test_invalid_prd_does_not_post_or_move_the_stage():
    orch, jira, _spy = _stack()

    class Blank:
        def draft(self, context):
            return PRD("", "", "", "", (), ())

        STOP_STAGE = Stage.PRD_REVIEW

    orch._product = Blank()
    with pytest.raises(ContractError):
        orch.run("PROJ-1")
    ticket = jira.get_ticket("PROJ-1")
    assert ticket.comments == ()
    assert ticket.stage is Stage.PRD_DRAFT


def test_resume_approved_advances_to_design_draft_without_a_design():
    orch, jira, _spy = _stack()
    orch.run("PROJ-1")
    result = orch.resume("PROJ-1", "approved", "Ready for design.")
    ticket = jira.get_ticket("PROJ-1")
    assert result.stage is Stage.DESIGN_DRAFT
    assert ticket.stage is Stage.DESIGN_DRAFT
    note = ticket.comments[-1]
    assert note.startswith("Decision: approved")
    assert "Ready for design." in note
    assert "## PRD" not in note
    assert "dependency_graph" not in note
    assert "### User flows" not in note
    with pytest.raises(OrchestratorError, match="only runs the product agent"):
        orch.run("PROJ-1")


def test_resume_changes_requested_returns_to_prd_draft_with_the_note():
    orch, jira, _spy = _stack()
    orch.run("PROJ-1")
    result = orch.resume("PROJ-1", "changes_requested", "Name the users.")
    ticket = jira.get_ticket("PROJ-1")
    assert result.stage is Stage.PRD_DRAFT
    assert result.decision == "changes_requested"
    assert ticket.stage is Stage.PRD_DRAFT
    assert "Name the users." in ticket.comments[-1]
    assert "Decision: changes_requested" in ticket.comments[-1]


def test_resume_rejects_a_decision_that_is_not_the_prd_gate():
    orch, jira, _spy = _stack()
    with pytest.raises(OrchestratorError, match="only from prd_review"):
        orch.resume("PROJ-1", "approved", "Too early.")
    assert jira.get_ticket("PROJ-1").comments == ()
    orch.run("PROJ-1")
    orch.resume("PROJ-1", "approved", "Ready for design.")
    with pytest.raises(OrchestratorError, match="only from prd_review"):
        orch.resume("PROJ-1", "approved", "Design is not this build.")
    assert jira.get_ticket("PROJ-1").stage is Stage.DESIGN_DRAFT


def test_rework_increments_the_prd_version():
    orch, jira, _spy = _stack()
    orch.run("PROJ-1")
    orch.resume("PROJ-1", "changes_requested", "Add users.")
    orch.run("PROJ-1")
    comments = jira.get_ticket("PROJ-1").comments
    assert "version: 1" in comments[0]
    assert "version: 2" in comments[2]


def test_cli_run_and_resume_exit_codes(capsys):
    orch, _jira, _spy = _stack()
    assert main(["run", "PROJ-1"], orchestrator=orch) == 0
    assert (
        main(
            ["resume", "PROJ-1", "changes_requested", "--note", "Name the users."],
            orchestrator=orch,
        )
        == 0
    )
    captured = capsys.readouterr()
    assert "posted PRD and set stage to prd_review" in captured.out
    assert "recorded changes_requested; stage is prd_draft" in captured.out
    orch.run("PROJ-1")
    orch.resume("PROJ-1", "approved", "Ready for design.")
    assert main(["run", "PROJ-1"], orchestrator=orch) == 1
    assert "only runs the product agent" in capsys.readouterr().err


def test_run_blocks_when_the_previous_gate_is_not_clear(monkeypatch):
    orch, jira, _spy = _stack()
    monkeypatch.setattr(
        "factory.orchestrator.previous_gate",
        lambda _stage: Stage.PRD_REVIEW,
    )
    with pytest.raises(OrchestratorError, match="until prd_review is approved"):
        orch.run("PROJ-1")
    assert jira.get_ticket("PROJ-1").comments == ()
