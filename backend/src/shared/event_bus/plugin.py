from typing import AsyncGenerator

from src.ioc import ioc
from .core import IEventBus
from .event_bus import InMemoryEventBus


__all__ = ['event_bus_plugin']


async def event_bus_plugin() -> AsyncGenerator:
    ioc.register(IEventBus, instance=InMemoryEventBus())

    yield
