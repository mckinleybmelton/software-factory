"""Deterministic orchestrator.

It reads the ticket stage, checks the previous gate, packs scoped context,
delegates to the product agent, and records the new stage. It does not write
PRD text. Design, architect, implementer, and reviewer do not run.
"""

from dataclasses import dataclass

from factory.context import pack_for_agent
from factory.contracts import render_prd, validate_prd
from factory.errors import OrchestratorError
from factory.jira import JiraClient
from factory.product import ProductAgent
from factory.stages import (
    ACTIVE_AGENTS,
    AGENT_BY_STAGE,
    AgentName,
    Stage,
    approve,
    previous_gate,
    reject,
    transition,
)


@dataclass(frozen=True)
class RunResult:
    key: str
    stage: Stage


@dataclass(frozen=True)
class ResumeResult:
    key: str
    stage: Stage
    decision: str


class Orchestrator:
    def __init__(self, jira: JiraClient, product: ProductAgent):
        self._jira = jira
        self._product = product

    def run(self, ticket_key: str) -> RunResult:
        """Draft a PRD when the ticket is at prd_draft, then stop at prd_review."""
        ticket = self._jira.get_ticket(ticket_key)
        stage = ticket.stage
        agent = _agent_for(stage)
        if agent not in ACTIVE_AGENTS:
            raise OrchestratorError(
                "This build only runs the product agent. "
                f"Ticket {ticket_key} is at '{stage.value}'."
            )
        gate = previous_gate(stage)
        if gate is not None:
            raise OrchestratorError(
                f"Cannot start {stage.value} until {gate.value} is approved."
            )
        context = pack_for_agent(agent, ticket)
        prd = self._product.draft(context)
        validate_prd(prd)
        move = transition(stage, self._product.STOP_STAGE)
        version = 1 + sum(1 for body in ticket.comments if body.startswith("## PRD"))
        comment = render_prd(prd) + _run_record(
            source=move.source,
            target=move.target,
            agent=agent,
            artifact="prd",
            version=version,
            previous=gate,
        )
        self._jira.post_comment(ticket_key, comment)
        self._jira.set_stage(ticket_key, move.target)
        return RunResult(key=ticket_key, stage=move.target)

    def resume(self, ticket_key: str, decision: str, note: str) -> ResumeResult:
        """Record a PRD gate decision. Does not generate a design."""
        if decision not in ("approved", "changes_requested"):
            raise OrchestratorError(
                "Decision must be 'approved' or 'changes_requested'."
            )
        if not note or not note.strip():
            raise OrchestratorError("A review note is required.")
        ticket = self._jira.get_ticket(ticket_key)
        if ticket.stage is not Stage.PRD_REVIEW:
            raise OrchestratorError(
                "Resume only records the PRD gate, and only from prd_review. "
                f"Ticket {ticket_key} is at '{ticket.stage.value}'."
            )
        move = approve(ticket.stage) if decision == "approved" else reject(ticket.stage)
        comment = f"Decision: {decision}\n\n{note.strip()}\n"
        self._jira.post_comment(ticket_key, comment)
        self._jira.set_stage(ticket_key, move.target)
        return ResumeResult(key=ticket_key, stage=move.target, decision=decision)


def _agent_for(stage: Stage) -> AgentName | None:
    return AGENT_BY_STAGE.get(stage)


def _run_record(
    *,
    source: Stage,
    target: Stage,
    agent: AgentName,
    artifact: str,
    version: int,
    previous: Stage | None,
) -> str:
    gate = "none" if previous is None else previous.value
    return (
        "---\n"
        f"stage: {source.value} -> {target.value}\n"
        f"agent: {agent.value}\n"
        f"artifact: {artifact}\n"
        f"version: {version}\n"
        f"previous_gate: {gate}\n"
    )
