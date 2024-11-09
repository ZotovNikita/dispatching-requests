from cent import AsyncClient, PublishRequest

from src.shared.event_bus import IEventHandler
from ..models import EmailEvent


__all__ = ['EmailEventHandler']


class EmailEventHandler(IEventHandler):
    def __init__(
        self,
        cent_client: AsyncClient,
    ) -> None:
        self._cent_client = cent_client

    async def __call__(self, event: EmailEvent) -> None:
        print(5555555555555)
        return
        await self._cent_client.publish(
            request=PublishRequest(
                channel=f'disp:demo',
                data=event.model_dump(mode='json'),
            ),
        )
