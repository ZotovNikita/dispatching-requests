from .event import Event


__all__ = ['IEventHandler']


class IEventHandler:
    async def __call__(self, event: Event) -> None:
        raise NotImplementedError
