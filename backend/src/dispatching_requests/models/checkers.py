from pydantic import BaseModel


class CheckSerialNumberResult(BaseModel):
    """Результат проверки на наличие серийных номеров"""
    success: bool
    data: list[str]
    text: str


class CheckCompletenessResult(BaseModel):
    """Результат проверки релевантности ответа пользователя указанным классам"""
    success: bool
    text: str


class CheckEquipmentNameResult(BaseModel):
    """Результат проверки на наличие названий моделей оборудования"""
    success: bool
    text: str
