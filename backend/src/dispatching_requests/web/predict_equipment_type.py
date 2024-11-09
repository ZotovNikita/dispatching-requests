import asyncio

from src.utils.nlu import (
    generate_prediction_equipment_type,
    tokenizer,
    model_embedding,
    model_classification_equipment_type,
)
from ..models import Email


class PredictEquipmentType:
    async def __call__(self, email: Email) -> str:
        equipment_type = await asyncio.to_thread(
            generate_prediction_equipment_type,
            topic=email.title,
            description=email.body,
            model=model_embedding,
            tokenizer=tokenizer,
            cb_model=model_classification_equipment_type,
        )

        return equipment_type
