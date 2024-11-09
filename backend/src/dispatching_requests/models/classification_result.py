from pydantic import BaseModel


class ClassificationResult(BaseModel):
    equipment_type: str
    point_of_failure: str
