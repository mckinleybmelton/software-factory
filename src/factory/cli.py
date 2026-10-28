"""Command line. `python -m factory run` and `python -m factory resume`."""

import argparse
import sys

from factory.config import load_settings
from factory.errors import FactoryError
from factory.jira import RestJira
from factory.orchestrator import Orchestrator
from factory.product import ProductAgent


def build_orchestrator(env: dict[str, str] | None = None) -> Orchestrator:
    settings = load_settings(env)
    return Orchestrator(jira=RestJira.from_settings(settings), product=ProductAgent())


def main(argv: list[str] | None = None, orchestrator: Orchestrator | None = None) -> int:
    parser = argparse.ArgumentParser(prog="factory")
    sub = parser.add_subparsers(dest="command", required=True)

    run_cmd = sub.add_parser(
        "run",
        help="Draft a PRD, post it on the ticket, and set the stage to prd_review",
    )
    run_cmd.add_argument("ticket_key")

    resume_cmd = sub.add_parser(
        "resume",
        help="Record approved or changes_requested on the PRD gate",
    )
    resume_cmd.add_argument("ticket_key")
    resume_cmd.add_argument("decision", choices=["approved", "changes_requested"])
    resume_cmd.add_argument("--note", required=True)

    args = parser.parse_args(argv)
    try:
        app = orchestrator if orchestrator is not None else build_orchestrator()
        if args.command == "run":
            result = app.run(args.ticket_key)
            print(f"{result.key}: posted PRD and set stage to {result.stage.value}")
        else:
            result = app.resume(args.ticket_key, args.decision, args.note)
            print(
                f"{result.key}: recorded {result.decision}; stage is {result.stage.value}"
            )
    except FactoryError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0
