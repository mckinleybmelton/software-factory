"""PRD contract validation, and typed stubs with no generators."""

from dataclasses import replace

import pytest

import factory.contracts as contracts
from factory.contracts import (
    ArchitectureArtifact,
    DesignArtifact,
    PRD,
    PRReviewPacket,
    render_prd,
    validate_prd,
)
from factory.errors import ContractError


def _valid() -> PRD:
    return PRD(
        problem="Rows are dropped.",
        users="Warehouse leads",
        scope="Nightly CSV export",
        out_of_scope="PDF reports",
        acceptance_criteria=("File lands in the bucket",),
        open_questions=("Which timezone?",),
    )


def test_valid_prd_passes():
    validate_prd(_valid())


@pytest.mark.parametrize("field", ["problem", "users", "scope", "out_of_scope"])
def test_blank_text_fields_fail(field: str):
    prd = replace(_valid(), **{field: "  "})
    with pytest.raises(ContractError, match=f"{field} is required"):
        validate_prd(prd)


def test_acceptance_criteria_are_required():
    with pytest.raises(ContractError, match="acceptance_criteria is required"):
        validate_prd(replace(_valid(), acceptance_criteria=()))
    with pytest.raises(ContractError, match="non-empty"):
        validate_prd(replace(_valid(), acceptance_criteria=(" ",)))


def test_open_questions_may_be_empty_but_not_blank_items():
    validate_prd(replace(_valid(), open_questions=()))
    with pytest.raises(ContractError, match="open_questions"):
        validate_prd(replace(_valid(), open_questions=("",)))


def test_render_includes_every_contract_field():
    body = render_prd(_valid())
    for text in (
        "## PRD",
        "### Problem",
        "Rows are dropped.",
        "### Users",
        "Warehouse leads",
        "### Scope",
        "Nightly CSV export",
        "### Out of scope",
        "PDF reports",
        "### Acceptance criteria",
        "- File lands in the bucket",
        "### Open questions",
        "- Which timezone?",
    ):
        assert text in body


def test_later_artifacts_are_typed_stubs_without_generators():
    design = DesignArtifact()
    architecture = ArchitectureArtifact()
    review = PRReviewPacket()
    assert design.user_flows == ()
    assert design.interfaces == ()
    assert architecture.components == ()
    assert architecture.boundaries == ()
    assert architecture.dependency_graph == ()
    assert review.matches == ()
    assert review.mismatches == ()
    assert review.pr_link == ""
    names = set(dir(contracts))
    assert "draft_design" not in names
    assert "draft_architecture" not in names
    assert "draft_review" not in names
    assert "generate_design" not in names
