import asyncio
import pandas as pd
from fastapi import File, UploadFile
from fastapi.responses import StreamingResponse
from io import BytesIO, StringIO

from src.utils.nlu import generate_predictions_from_dataframe, model_embedding, tokenizer, model_classification_equipment_type


class PredictFile:
    async def __call__(self, file: UploadFile = File(...)) -> None:
        try:
            contents = await file.read()
        finally:
            await file.close()

        def proccess(content: bytes) -> str:
            data = BytesIO(content)
            csv = pd.read_csv(data)

            preds = generate_predictions_from_dataframe(csv, model_embedding, tokenizer, model_classification_equipment_type)

            stream = StringIO()
            pd.DataFrame([preds]).T.to_csv(stream, index=False)

            return stream.getvalue()

        data = await asyncio.to_thread(proccess, content=contents)

        return StreamingResponse(
            iter([data]),
            media_type='text/csv',
            headers={
                'Content-Disposition': 'attachment;filename=submission.csv',
            }
        )
