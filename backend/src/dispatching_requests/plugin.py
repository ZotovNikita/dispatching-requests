from typing import AsyncGenerator, get_type_hints

from fastapi import FastAPI
from langgraph.graph import StateGraph
from cent import AsyncClient

from src.ioc import ioc
from src.settings import Settings
from src.shared.event_bus import IEventBus
from .models import EmailEvent
from .handlers import EmailEventHandler
from .graph import State, graph_initialize
from .web import HandleEmail, PredictEmail, PredictEquipmentType, PredictFailurePoint


__all__ = ['dispatching_requests_plugin']


async def dispatching_requests_plugin(settings: Settings) -> AsyncGenerator:
    """
    Плагин для создания моделей и самого dispatching_requests'а.
    """
    fastapi = ioc.resolve(FastAPI)
    event_bus = ioc.resolve(IEventBus)

    # При более детальной разработке стоит вынести добавление центрифуги в отдельный плагин
    cent_client = AsyncClient(
        api_url=settings.centrifugo.api_url,
        api_key=settings.centrifugo.api_key,
    )

    # Подписка на событие: когда система пубюликует событие EmailEvent, оно будет отправляться в центрифугу с помощью EmailEventHandler
    await event_bus.subscribe(
        event=EmailEvent,
        handler=EmailEventHandler(cent_client),
    )

    # Создание графа для диспетчеризации
    workflow = StateGraph(State)
    graph = graph_initialize(workflow)

    handle_email_view = HandleEmail(  # ручка
        graph=graph,
        event_bus=event_bus,
    )
    fastapi.add_api_route(  # добавление ручки
        path='/email/handle',
        name='Диспетчиризировать обращение клиента',
        tags=['Email'],
        methods=['POST'],
        endpoint=handle_email_view.__call__,
        response_model=get_type_hints(handle_email_view.__call__)['return'],
    )

    predict_email_view = PredictEmail()
    fastapi.add_api_route(
        path='/email/predict',
        name='Получить набор предсказаний для обращения клиента',
        tags=['Email'],
        methods=['POST'],
        endpoint=predict_email_view.__call__,
        response_model=get_type_hints(predict_email_view.__call__)['return'],
    )

    predict_equipment_type_view = PredictEquipmentType()
    fastapi.add_api_route(
        path='/predict/equipment_type',
        name='Предсказать тип оборудования',
        tags=['Predict'],
        methods=['POST'],
        endpoint=predict_equipment_type_view.__call__,
        response_model=get_type_hints(predict_equipment_type_view.__call__)['return'],
    )

    predict_failure_point_view = PredictFailurePoint()
    fastapi.add_api_route(
        path='/predict/failure_point',
        name='Предсказать точку отказа',
        tags=['Predict'],
        methods=['POST'],
        endpoint=predict_failure_point_view.__call__,
        response_model=get_type_hints(predict_failure_point_view.__call__)['return'],
    )

    yield
