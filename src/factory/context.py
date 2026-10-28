"""Context packer. Each agent sees only the ticket slice it needs."""

from dataclasses import dataclass

from factory.jira import Ticket
from factory.stages import AgentName, Stage


@dataclass(frozen=True)
class TicketSlice:
    """Fields the product agent may read. No comments and no other transcripts."""

    key: str
    summary: str
    description: str
    stage: Stage


def pack_product_context(ticket: Ticket) -> TicketSlice:
    """Pack the product agent's input. Other agents' transcripts are not included."""
    if not isinstance(ticket, Ticket):
        raise TypeError("pack_product_context expects a ticket snapshot.")
    return TicketSlice(
        key=ticket.key,
        summary=ticket.summary,
        description=ticket.description,
        stage=ticket.stage,
    )


def pack_for_agent(agent: AgentName, ticket: Ticket) -> TicketSlice:
    """Dispatch packing. This build only packs context for the product agent."""
    if agent is not AgentName.PRODUCT:
        raise ValueError(
            f"This build only packs context for the product agent, not {agent.value}."
        )
    return pack_product_context(ticket)
