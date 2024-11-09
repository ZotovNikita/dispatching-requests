from typing_extensions import TypedDict

from ..models import Email, ClassificationResult, CheckSerialNumberResult, CheckCompletenessResult, CheckEquipmentNameResult, EmailEvent


class State(TypedDict):
    email: Email
    classification_result: ClassificationResult
    serial_number_check_result: CheckSerialNumberResult
    completeness_check_result: CheckCompletenessResult
    equipment_name_check_result: CheckEquipmentNameResult
    event: EmailEvent
