from typing import AsyncGenerator

from pydantic import BaseModel
from src.ioc import ioc
from src.settings import Settings

from fastapi import FastAPI

__all__ = ['dispatching_requests_plugin']


class Email(BaseModel):
    title: str
    body: str


class DispatcherRequest(BaseModel):
    serial_number: str
    type_of_equipment: str


async def dispatching_requests_plugin(settings: Settings) -> AsyncGenerator:
    """
    Плагин для создания моделей и самого dispatching_requests'а.
    """
    fastapi = ioc.resolve(FastAPI)

    # QA

    # модель для создания эмбеддинго

    @fastapi.post(
        '/message',
        tags=['QA'],
        name='Получить дипетчеризацию заявки',
        description='Получить дипетчеризацию заявки',
    )
    async def message(request: Email) -> DispatcherRequest:
        return DispatcherRequest(
            serial_number='123',
            type_of_equipment='popa'
        )

    yield