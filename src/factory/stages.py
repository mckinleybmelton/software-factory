"""Stage machine. Later agents are named here and do not run in this build."""

from enum import StrEnum
from typing import Iterable, Mapping

from factory.errors import AmbiguousStage, IllegalTransition


class Stage(StrEnum):
    PRD_DRAFT = "prd_draft"
    PRD_REVIEW = "prd_review"
    DESIGN_DRAFT = "design_draft"
    DESIGN_REVIEW = "design_review"
    ARCHITECTURE_DRAFT = "architecture_draft"
    ARCHITECTURE_REVIEW = "architecture_review"
    IMPLEMENTATION = "implementation"
    PR_REVIEW = "pr_review"
    DONE = "done"


class AgentName(StrEnum):
    PRODUCT = "product"
    DESIGN = "design"
    ARCHITECT = "architect"
    IMPLEMENTER = "implementer"
    REVIEWER = "reviewer"


class TransitionKind(StrEnum):
    SUBMIT = "submit"
    APPROVE = "approve"
    REJECT = "reject"


# Specialists the orchestrator knows. Only the product agent runs in this build.
NAMED_AGENTS: tuple[AgentName, ...] = (
    AgentName.PRODUCT,
    AgentName.DESIGN,
    AgentName.ARCHITECT,
    AgentName.IMPLEMENTER,
    AgentName.REVIEWER,
)

AGENT_BY_STAGE: dict[Stage, AgentName] = {
    Stage.PRD_DRAFT: AgentName.PRODUCT,
    Stage.DESIGN_DRAFT: AgentName.DESIGN,
    Stage.ARCHITECTURE_DRAFT: AgentName.ARCHITECT,
    Stage.IMPLEMENTATION: AgentName.IMPLEMENTER,
    Stage.PR_REVIEW: AgentName.REVIEWER,
}

ACTIVE_AGENTS: frozenset[AgentName] = frozenset({AgentName.PRODUCT})


class Transition:
    """One allowed move. Rejection notes are stored on the ticket, not here."""

    def __init__(self, source: Stage, target: Stage, kind: TransitionKind):
        self.source = source
        self.target = target
        self.kind = kind


# Draft or implementation submits work into its review.
_SUBMIT: dict[Stage, Stage] = {
    Stage.PRD_DRAFT: Stage.PRD_REVIEW,
    Stage.DESIGN_DRAFT: Stage.DESIGN_REVIEW,
    Stage.ARCHITECTURE_DRAFT: Stage.ARCHITECTURE_REVIEW,
    Stage.IMPLEMENTATION: Stage.PR_REVIEW,
}

# Approval is the only way into the next stage.
_APPROVE: dict[Stage, Stage] = {
    Stage.PRD_REVIEW: Stage.DESIGN_DRAFT,
    Stage.DESIGN_REVIEW: Stage.ARCHITECTURE_DRAFT,
    Stage.ARCHITECTURE_REVIEW: Stage.IMPLEMENTATION,
    Stage.PR_REVIEW: Stage.DONE,
}

# Rejection returns that same stage to its draft (implementation, for a PR).
_REJECT: dict[Stage, Stage] = {
    Stage.PRD_REVIEW: Stage.PRD_DRAFT,
    Stage.DESIGN_REVIEW: Stage.DESIGN_DRAFT,
    Stage.ARCHITECTURE_REVIEW: Stage.ARCHITECTURE_DRAFT,
    Stage.PR_REVIEW: Stage.IMPLEMENTATION,
}

# Human gate that must already be approved before work at this stage starts.
# None is the factory entry: a missing label is treated as prd_draft.
_PREVIOUS_GATE: dict[Stage, Stage | None] = {
    Stage.PRD_DRAFT: None,
    Stage.PRD_REVIEW: None,
    Stage.DESIGN_DRAFT: Stage.PRD_REVIEW,
    Stage.DESIGN_REVIEW: Stage.PRD_REVIEW,
    Stage.ARCHITECTURE_DRAFT: Stage.DESIGN_REVIEW,
    Stage.ARCHITECTURE_REVIEW: Stage.DESIGN_REVIEW,
    Stage.IMPLEMENTATION: Stage.ARCHITECTURE_REVIEW,
    Stage.PR_REVIEW: Stage.ARCHITECTURE_REVIEW,
    Stage.DONE: Stage.PR_REVIEW,
}


def previous_gate(stage: Stage) -> Stage | None:
    """Return the review that must be approved before `stage` can start."""
    return _PREVIOUS_GATE[stage]


def allowed_transitions() -> frozenset[tuple[Stage, Stage]]:
    pairs: set[tuple[Stage, Stage]] = set()
    for table in (_SUBMIT, _APPROVE, _REJECT):
        for source, target in table.items():
            pairs.add((source, target))
    return frozenset(pairs)


def transition(source: Stage, target: Stage) -> Transition:
    """Return the move, or raise if this edge is not allowed."""
    if _SUBMIT.get(source) is target:
        kind = TransitionKind.SUBMIT
    elif _APPROVE.get(source) is target:
        kind = TransitionKind.APPROVE
    elif _REJECT.get(source) is target:
        kind = TransitionKind.REJECT
    else:
        raise IllegalTransition(
            f"Transition {source.value} -> {target.value} is not allowed."
        )
    return Transition(source, target, kind)


def approve(source: Stage) -> Transition:
    """Advance a review stage. This is the only entry to the next stage."""
    target = _APPROVE.get(source)
    if target is None:
        raise IllegalTransition(f"Stage {source.value} has no approval transition.")
    return transition(source, target)


def reject(source: Stage) -> Transition:
    """Return a review stage to its draft. The caller stores the reviewer's notes."""
    target = _REJECT.get(source)
    if target is None:
        raise IllegalTransition(f"Stage {source.value} cannot be rejected to a draft.")
    return transition(source, target)


def stage_from_labels(labels: Iterable[str], stage_labels: Mapping[Stage, str]) -> Stage:
    """Resolve the current stage from ticket labels.

    No stage label means prd_draft. Any other labels are ignored.
    """
    reverse = {label: stage for stage, label in stage_labels.items()}
    found: list[Stage] = []
    for label in labels:
        stage = reverse.get(label)
        if stage is not None and stage not in found:
            found.append(stage)
    if not found:
        return Stage.PRD_DRAFT
    if len(found) > 1:
        names = ", ".join(stage.value for stage in found)
        raise AmbiguousStage(f"Ticket has more than one stage label: {names}.")
    return found[0]
