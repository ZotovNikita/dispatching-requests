import asyncio
import pandas as pd
from fastapi import File, UploadFile
from fastapi.responses import StreamingResponse
from io import BytesIO, StringIO

from src.utils.nlu import (
    generate_predictions_from_dataframe,
    model_embedding,
    tokenizer,
    model_classification_equipment_type,
    model_classification_failure_point,
    label_encoder,
)


class PredictFile:
    async def __call__(self, file: UploadFile = File(...)) -> None:
        try:
            contents = await file.read()
        finally:
            await file.close()

        def proccess(content: bytes) -> str:
            data = BytesIO(content)
            csv = pd.read_csv(data)
            csv['Описание'] = csv['Описание'].str.replace('_x000D_', '', regex=False)

            preds = generate_predictions_from_dataframe(
                df=csv,
                model_embedding=model_embedding,
                tokenizer=tokenizer,
                cb_model=model_classification_equipment_type,
                model_onnx=model_classification_failure_point,
                label_encoder=label_encoder,
            )

            stream = StringIO()
            preds.to_csv(stream, index=True, index_label='index')

            return stream.getvalue()

        data = await asyncio.to_thread(proccess, content=contents)

        return StreamingResponse(
            iter([data]),
            media_type='text/csv',
            headers={
                'Content-Disposition': 'attachment;filename=submission.csv',
            }
        )
