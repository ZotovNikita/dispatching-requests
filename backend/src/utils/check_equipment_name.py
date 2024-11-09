import os

from langchain_ollama.llms import OllamaLLM
from langchain.prompts import ChatPromptTemplate

from .templates import CHECK_EQUIPMENT_NAME_TEMPLATE


_prompt = ChatPromptTemplate.from_template(CHECK_EQUIPMENT_NAME_TEMPLATE)

_llm = OllamaLLM(
    model='gemma2:9b',
    base_url=os.getenv('LLM_MODEL_URL'),  # Url адрес модели
    temperature=0,
    format='json',
    num_ctx=8192,
    num_predict=128,
)

_chain = _prompt | _llm


async def check_equipment_name(title: str, body: str) -> str:
    """ Проверяет с помощью модель gemma2 есть ли в тексте названия оборудования
    Args:
        title (str): Заголовок письма
        body (str): Текст письма

    Returns:
        str: Результат работы модели в виде json
        {
            'flag': ...,
            'answer': ...
        }, где flag (boolean) - true значит, что название присутствует, flag - false, что отсутствует
        answer (str) - ответный запрос модели, (непустой, если flag - false).
    """

    return await _chain.ainvoke({
        'title': title,
        'body': body
    })
