from pydantic import BaseModel


class DispatchingResponse(BaseModel):
    equipment_type: str
    failure_point: str
    serial_numbers: list[str]
