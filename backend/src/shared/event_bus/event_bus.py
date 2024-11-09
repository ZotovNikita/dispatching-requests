from collections import defaultdict
from typing import List, MutableMapping, Type

from .core import Event, IEventBus, IEventHandler


__all__ = ['InMemoryEventBus']


class InMemoryEventBus(IEventBus):
    def __init__(self) -> None:
        self.event_handlers: MutableMapping[Type[Event], List[IEventHandler]] = defaultdict(list)

    async def subscribe(self, event: Type[Event], handler: IEventHandler) -> None:
        self.event_handlers[event].append(handler)

    async def publish(self, event: Event) -> None:
        for handler in self.event_handlers[type(event)]:
            await handler(event)
