from langchain_ollama.llms import OllamaLLM
from langchain.prompts import ChatPromptTemplate


def check_eq_name(llm_model_url: str, title: str, body: str, type_of_equipment : str, fail_point: str) -> str:
    """ Проверяет с помощью модель gemma2 полна ли информация в сообщении
    Args:
        llm_model_url (str): Url адрес модели.
        title (str): Заголовок письма
        body(str): Текст письма
        type_of_equipment(str): Тип оборудования(определен классификаторами)
        fail_point(str): Точка отказа(определена классификаторами)

    Returns:
        str: Результат работы модели в виде json
        {
            'flag': ...,
            'answer': ...,
        }, где flag(boolean) - true значит, что название присутствует, flag - false, что отсутствует
        answer(str) - ответный запрос модели (непустой, если flag - false).
    """
    template = """Представь, что ты помощник специалиста пользовательской поддержки компании по производству и обслуживанию технического оборудования.

    Тебе поступило письмо по электронной почте от клиента.

    Заголовок письма: {title}.

    Текст письма: {body}.

    Проанализируй, достаточно ли информации из письма для того, чтобы подтвердить предоложение, что проблема с оборудованием {type_of_equipment}, а также его частью {fail_point}. 

    Отсутствия модели оборудования в сообщении не является признаком недостаточности информации. НИКОГДА не спрашивай о ней клиентов.

    Ответ напиши в виде json-файла, в котором будет поле flag и поле answer.

    Если ты считаешь, что информации достаточно для того, чтобы понять, что проблема с оборудованием {type_of_equipment}, а также его частью {fail_point}, тогда в поле flag напиши true, а поле answer сделай пустым.

    Если ты считаешь, что информации не достаточно для того, чтобы понять, что проблема с оборудованием {type_of_equipment}, а также его частью {fail_point}, тогда в поле flag напиши false, а в поле answer напиши с точки зрения оператора поддержки, что необходимо добавить в письме, чтобы оно стало понятным.
    Отвечай так, как если бы ты лично общалась с клиентом. Будь вежливой, поздоровайся с ним.

    Следуй инструкциям, отвечай кратко. В ответе кроме json-файла ничего писать не нужно.

    Структура ответа:

    {{
    "flag": ...,
    "answer": ...
    }}
    """

    prompt = ChatPromptTemplate.from_template(template)

    llm = OllamaLLM(
        model='gemma2',
        base_url=llm_model_url,
        temperature=0,
        format='json',
        num_ctx=8192,
        num_predict=128,
    )

    chain_ = prompt | llm

    return chain_.invoke({
            'title': title,
            'body': body,
            'type_of_equipment': type_of_equipment,
            'fail_point': fail_point,
        })
