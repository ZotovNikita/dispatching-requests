from ..models import ClassificationResult, CheckSerialNumberResult, CheckCompletenessResult, CheckEquipmentNameResult, EmailEvent
from .state import State
from src.utils.ner import get_all_serial_numbers


async def email_classification(state: State):
    email = state['email']

    cls1 = email.title
    cls2 = 'cls2'

    return {
        'classification_result': ClassificationResult(
            equipment_type=cls1,
            point_of_failure=cls2,
        ),
    }


async def serial_number_check(state: State):
    email = state['email']

    default_value = 'Уточнить'

    ners = get_all_serial_numbers(
        header=email.title,
        body=email.body,
        default_value=default_value,
    )

    return {
        'serial_number_check_result': CheckSerialNumberResult(
            success=default_value in ners,
            data=ners,
            text='1',
        ),
    }


async def completeness_check(state: State):
    email = state['email']
    classification_result = state['classification_result']

    s = True
    d = 'data'

    return {
        'completeness_check_result': CheckCompletenessResult(
            success=s,
            data=d,
            text='2',
        ),
    }


async def equipment_name_check(state: State):
    email = state['email']
    classification_result = state['classification_result']

    s = True
    d = 'data'

    return {
        'equipment_name_check_result': CheckEquipmentNameResult(
            success=s,
            data=d,
            text='3',
        ),
    }


async def checks_inspection(state: State):
    serial_number_check_result = state['serial_number_check_result']
    completeness_check_result = state['completeness_check_result']
    equipment_name_check_result = state['equipment_name_check_result']

    inspection_result: bool = serial_number_check_result.success and (completeness_check_result.success or equipment_name_check_result.success)

    return {
        'event': EmailEvent(
            type='to_agent' if inspection_result else 'resending',
            email=state['email'],
            classification_result=state['classification_result'],
            serial_number_check_result=state['serial_number_check_result'],
            completeness_check_result=state['completeness_check_result'],
            equipment_name_check_result=state['equipment_name_check_result'],
        ),
    }
