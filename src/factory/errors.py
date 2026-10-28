"""Errors the CLI prints without a traceback."""


class FactoryError(Exception):
    """Base error for expected factory failures."""


class ConfigError(FactoryError):
    """Environment or stage-label configuration is missing or invalid."""


class IllegalTransition(FactoryError):
    """A stage change is not in the allowed set."""


class AmbiguousStage(FactoryError):
    """A ticket carries more than one stage label."""


class ContractError(FactoryError):
    """An artifact does not satisfy its contract."""

    def __init__(self, errors: list[str]):
        self.errors = errors
        super().__init__("PRD contract invalid: " + "; ".join(errors))


class JiraError(FactoryError):
    """The Jira adapter could not read or write a ticket."""


class OrchestratorError(FactoryError):
    """The orchestrator refused to run or resume."""
