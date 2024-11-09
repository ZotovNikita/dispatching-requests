from typing import Type

from .event import Event
from .handler import IEventHandler


__all__ = ['IEventBus']


class IEventBus:
    async def subscribe(self, event: Type[Event], handler: IEventHandler) -> None:
        raise NotImplementedError

    async def publish(self, event: Event) -> None:
        raise NotImplementedError
