from langgraph.graph.state import CompiledStateGraph

from src.shared.event_bus import IEventBus
from ..models import Email, EmailEvent


class HandleEmail:
    def __init__(self, graph: CompiledStateGraph, event_bus: IEventBus) -> None:
        self._graph = graph
        self._event_bus = event_bus

    async def __call__(self, email: Email) -> EmailEvent:
        state = await self._graph.ainvoke({'email': email})
        event: EmailEvent = state['event']

        await self._event_bus.publish(event)

        return event
