from typing import Literal

from pydantic import BaseModel

from ..models import Email, ClassificationResult, CheckSerialNumberResult, CheckCompletenessResult, CheckEquipmentNameResult


class EmailEvent(BaseModel):
    type: Literal['resending', 'to_agent']
    email: Email
    classification_result: ClassificationResult
    serial_number_check_result: CheckSerialNumberResult | None = None
    completeness_check_result: CheckCompletenessResult | None = None
    equipment_name_check_result: CheckEquipmentNameResult | None = None
