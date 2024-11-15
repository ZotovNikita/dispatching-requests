import asyncio

from src.utils.nlu import (
    generate_prediction_equipment_type,
    generate_prediction_failure_point,
    tokenizer,
    model_embedding,
    model_classification_equipment_type,
    label_encoder,
    model_classification_failure_point,
)
from src.utils.ner import get_all_serial_numbers
from ..models import Email, DispatchingResponse


class PredictEmail:
    async def __call__(self, email: Email) -> DispatchingResponse:
        equipment_type = await asyncio.to_thread(
            generate_prediction_equipment_type,
            topic=email.title,
            description=email.body,
            model=model_embedding,
            tokenizer=tokenizer,
            cb_model=model_classification_equipment_type,
        )
        failure_point = await asyncio.to_thread(
            generate_prediction_failure_point,
            topic=email.title,
            description=email.body,
            model_embedding=model_embedding,
            tokenizer=tokenizer,
            model_onnx=model_classification_failure_point,
            label_encoder=label_encoder,
        )
        serial_numbers = await asyncio.to_thread(
            get_all_serial_numbers,
            header=email.title,
            body=email.body,
        )

        return DispatchingResponse(
            id=email.id,
            equipment_type=equipment_type,
            failure_point=failure_point,
            serial_numbers=serial_numbers,
        )
