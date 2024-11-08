from collections.abc import AsyncGenerator
import contextlib
from typing import List


__all__ = ['App']


class App:
    """
    Абстракция приложения. Определены операции для добавления плагинов, запуска и остановки приложения.
    
    Абстракция с плагинами реализована в виде асинхронных генераторов.
    """
    __slots__ = ('_plugins',)

    def __init__(self) -> None:
        self._plugins: List[AsyncGenerator] = []

    def add_plugin(self, plugin: AsyncGenerator) -> None:
        self._plugins.append(plugin)

    async def startapp(self) -> None:
        for plugin in self._plugins:
            await plugin.__anext__()

    async def shutdown(self) -> None:
        for plugin in self._plugins:
            with contextlib.suppress(StopAsyncIteration):
                await plugin.__anext__()