"""Stage machine: allowed edges, rejections, and the stage label map."""

import pytest

from factory.config import default_stage_labels, resolve_stage_labels
from factory.errors import AmbiguousStage, ConfigError, IllegalTransition
from factory.stages import (
    ACTIVE_AGENTS,
    NAMED_AGENTS,
    AgentName,
    Stage,
    TransitionKind,
    allowed_transitions,
    approve,
    previous_gate,
    reject,
    stage_from_labels,
    transition,
)


def test_named_agents_include_later_specialists_that_do_not_run():
    assert set(NAMED_AGENTS) == {
        AgentName.PRODUCT,
        AgentName.DESIGN,
        AgentName.ARCHITECT,
        AgentName.IMPLEMENTER,
        AgentName.REVIEWER,
    }
    assert ACTIVE_AGENTS == frozenset({AgentName.PRODUCT})


def test_allowed_transitions_cover_submit_approve_and_reject():
    cases = [
        (Stage.PRD_DRAFT, Stage.PRD_REVIEW, TransitionKind.SUBMIT),
        (Stage.PRD_REVIEW, Stage.DESIGN_DRAFT, TransitionKind.APPROVE),
        (Stage.PRD_REVIEW, Stage.PRD_DRAFT, TransitionKind.REJECT),
        (Stage.DESIGN_DRAFT, Stage.DESIGN_REVIEW, TransitionKind.SUBMIT),
        (Stage.DESIGN_REVIEW, Stage.ARCHITECTURE_DRAFT, TransitionKind.APPROVE),
        (Stage.DESIGN_REVIEW, Stage.DESIGN_DRAFT, TransitionKind.REJECT),
        (Stage.ARCHITECTURE_DRAFT, Stage.ARCHITECTURE_REVIEW, TransitionKind.SUBMIT),
        (Stage.ARCHITECTURE_REVIEW, Stage.IMPLEMENTATION, TransitionKind.APPROVE),
        (Stage.ARCHITECTURE_REVIEW, Stage.ARCHITECTURE_DRAFT, TransitionKind.REJECT),
        (Stage.IMPLEMENTATION, Stage.PR_REVIEW, TransitionKind.SUBMIT),
        (Stage.PR_REVIEW, Stage.DONE, TransitionKind.APPROVE),
        (Stage.PR_REVIEW, Stage.IMPLEMENTATION, TransitionKind.REJECT),
    ]
    assert len(cases) == len(allowed_transitions())
    for source, target, kind in cases:
        move = transition(source, target)
        assert move.source is source
        assert move.target is target
        assert move.kind is kind


def test_rejected_transitions_cannot_skip_a_gate():
    rejected = [
        (Stage.PRD_DRAFT, Stage.DESIGN_DRAFT),
        (Stage.PRD_DRAFT, Stage.DESIGN_REVIEW),
        (Stage.PRD_DRAFT, Stage.DONE),
        (Stage.PRD_DRAFT, Stage.PRD_DRAFT),
        (Stage.PRD_REVIEW, Stage.ARCHITECTURE_DRAFT),
        (Stage.PRD_REVIEW, Stage.IMPLEMENTATION),
        (Stage.PRD_REVIEW, Stage.PRD_REVIEW),
        (Stage.DESIGN_DRAFT, Stage.ARCHITECTURE_DRAFT),
        (Stage.DESIGN_DRAFT, Stage.PRD_DRAFT),
        (Stage.DESIGN_REVIEW, Stage.IMPLEMENTATION),
        (Stage.ARCHITECTURE_DRAFT, Stage.PR_REVIEW),
        (Stage.IMPLEMENTATION, Stage.DONE),
        (Stage.IMPLEMENTATION, Stage.ARCHITECTURE_DRAFT),
        (Stage.PR_REVIEW, Stage.PRD_DRAFT),
        (Stage.DONE, Stage.PRD_DRAFT),
        (Stage.DONE, Stage.PR_REVIEW),
    ]
    for source, target in rejected:
        with pytest.raises(IllegalTransition):
            transition(source, target)


def test_rejection_returns_the_same_stage_to_its_draft():
    assert reject(Stage.PRD_REVIEW).target is Stage.PRD_DRAFT
    assert reject(Stage.DESIGN_REVIEW).target is Stage.DESIGN_DRAFT
    assert reject(Stage.ARCHITECTURE_REVIEW).target is Stage.ARCHITECTURE_DRAFT
    assert reject(Stage.PR_REVIEW).target is Stage.IMPLEMENTATION
    with pytest.raises(IllegalTransition):
        reject(Stage.PRD_DRAFT)
    with pytest.raises(IllegalTransition):
        approve(Stage.PRD_DRAFT)


def test_later_stages_require_the_previous_gate():
    assert previous_gate(Stage.PRD_DRAFT) is None
    assert previous_gate(Stage.PRD_REVIEW) is None
    assert previous_gate(Stage.DESIGN_DRAFT) is Stage.PRD_REVIEW
    assert previous_gate(Stage.ARCHITECTURE_DRAFT) is Stage.DESIGN_REVIEW
    assert previous_gate(Stage.IMPLEMENTATION) is Stage.ARCHITECTURE_REVIEW
    assert previous_gate(Stage.DONE) is Stage.PR_REVIEW
    assert approve(Stage.PRD_REVIEW).target is Stage.DESIGN_DRAFT
    assert approve(Stage.DESIGN_REVIEW).target is Stage.ARCHITECTURE_DRAFT
    assert approve(Stage.ARCHITECTURE_REVIEW).target is Stage.IMPLEMENTATION


def test_missing_stage_label_is_prd_draft():
    labels = default_stage_labels()
    assert stage_from_labels([], labels) is Stage.PRD_DRAFT
    assert stage_from_labels(["bug", "backend"], labels) is Stage.PRD_DRAFT
    assert stage_from_labels(["prd_review"], labels) is Stage.PRD_REVIEW


def test_stage_label_defaults_match_state_names_and_config_can_override():
    labels = default_stage_labels()
    assert labels[Stage.DESIGN_DRAFT] == "design_draft"
    assert labels[Stage.PR_REVIEW] == "pr_review"
    overridden = resolve_stage_labels({"prd_review": "sf-prd-review"})
    assert overridden[Stage.PRD_DRAFT] == "prd_draft"
    assert overridden[Stage.PRD_REVIEW] == "sf-prd-review"
    assert stage_from_labels(["sf-prd-review"], overridden) is Stage.PRD_REVIEW


def test_label_map_rejects_unknown_stages_and_duplicates():
    with pytest.raises(ConfigError, match="Unknown stage"):
        resolve_stage_labels({"shipped": "done"})
    with pytest.raises(ConfigError, match="used for both"):
        resolve_stage_labels({"prd_draft": "prd_review"})


def test_multiple_stage_labels_are_rejected():
    with pytest.raises(AmbiguousStage):
        stage_from_labels(["prd_draft", "prd_review"], default_stage_labels())
