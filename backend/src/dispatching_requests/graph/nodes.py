import asyncio

import ujson
from src.utils.ner import get_all_serial_numbers
from src.utils.nlu import (
    generate_prediction_equipment_type,
    generate_prediction_failure_point,
    tokenizer,
    model_embedding,
    model_classification_equipment_type,
    label_encoder,
    model_classification_failure_point,
)
from src.utils.check_complete_information import check_complete_information
from src.utils.check_equipment_name import check_equipment_name
from ..models import (
    ClassificationResult,
    CheckSerialNumberResult,
    CheckCompletenessResult,
    CheckEquipmentNameResult,
    EmailEvent,
)
from .state import State


async def email_classification(state: State):
    email = state['email']

    loop = asyncio.get_running_loop()

    equipment_type = await loop.run_in_executor(
        None,
        generate_prediction_equipment_type,
        email.title,
        email.body,
        model_embedding,
        tokenizer,
        model_classification_equipment_type,
    )
    point_of_failure = await loop.run_in_executor(
        None,
        generate_prediction_failure_point,
        email.title,
        email.body,
        model_embedding,
        tokenizer,
        model_classification_failure_point,
        label_encoder,
    )

    return {
        'classification_result': ClassificationResult(
            equipment_type=equipment_type,
            point_of_failure=point_of_failure,
        ),
    }


async def serial_number_check(state: State):
    email = state['email']

    default_value = 'Уточнить'

    ners = await asyncio.to_thread(
        get_all_serial_numbers,
        header=email.title,
        body=email.body,
        default_value=default_value,
    )

    return {
        'serial_number_check_result': CheckSerialNumberResult(
            success=default_value not in ners,
            data=ners,
            text='Необходимо указать серийные номера.',
        ),
    }


async def completeness_check(state: State):
    email = state['email']
    classification_result = state['classification_result']

    llm_answer = await check_complete_information(
        title=email.title,
        body=email.body,
        type_of_equipment=classification_result.equipment_type,
        fail_point=classification_result.point_of_failure,
    )
    data = {
        'flag': True,
        'answer': '',
    }

    try:
        data = ujson.loads(llm_answer)
    except:
        pass

    return {
        'completeness_check_result': CheckCompletenessResult(
            success=data.get('flag', True),
            text=data.get('answer', ''),
        ),
    }


async def equipment_name_check(state: State):
    email = state['email']

    llm_answer = await check_equipment_name(
        title=email.title,
        body=email.body,
    )
    data = {
        'flag': True,
        'answer': '',
    }

    try:
        data = ujson.loads(llm_answer)
    except:
        pass

    return {
        'equipment_name_check_result': CheckEquipmentNameResult(
            success=data.get('flag', True),
            text=data.get('answer', ''),
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
