from pydantic import BaseModel


class DispatchingResponse(BaseModel):
    id: str | None = None
    equipment_type: str
    failure_point: str
    serial_numbers: list[str]
