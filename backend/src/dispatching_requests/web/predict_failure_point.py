import asyncio

from src.utils.nlu import (
    generate_prediction_failure_point,
    tokenizer,
    model_embedding,
    label_encoder,
    model_classification_failure_point,
)
from ..models import Email


class PredictFailurePoint:
    async def __call__(self, email: Email) -> str:
        failure_point = await asyncio.to_thread(
            generate_prediction_failure_point,
            topic=email.title,
            description=email.body,
            model_embedding=model_embedding,
            tokenizer=tokenizer,
            model_onnx=model_classification_failure_point,
            label_encoder=label_encoder,
        )

        return failure_point
