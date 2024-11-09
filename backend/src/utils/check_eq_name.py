from langchain_ollama.llms import OllamaLLM
from langchain.prompts import ChatPromptTemplate


def check_eq_name(llm_model_url: str, title: str, body: str) -> str:
    """ Проверяет с помощью модель gemma2 есть ли в тексте названия оборудования
    Args:
        llm_model_url (str): Url адрес модели.
        title (str): Заголовок письма
        body(str): Текст письма

    Returns:
        str: Результат работы модели в виде json
        {
            'flag': ...,
            'answer': ...,
        }, где flag(boolean) - true значит, что название присутствует, flag - false, что отсутствует
        answer(str) - ответный запрос модели, если flag - false.
    """
    template = """Представь, что ты помощник специалиста пользовательской поддержки компании по производству и обслуживанию технического оборудования.

    Тебе поступило письмо по электронной почте от клиента.

    Заголовок письма: {title}.

    Текст письма: {body}.

    Проанализируй, достаточно ли информации из письма для того, чтобы узнать название модели оборудования. Пример названия модели оборудования: НК2-1404 или CX-1015-12.
    Оно также может быть окружено символами //.

    Ответ напиши в виде json-файла, в котором будет поле flag и поле answer.

    Если ты считаешь, что информации достаточно для того, чтобы понять название модели оборудования, тогда в поле flag напиши True, а поле answer сделай пустым.

    Если ты считаешь, что информации не достаточно для того, чтобы понять название модели оборудования, тогда в поле flag напиши False, а в поле answer напиши с точки зрения оператора поддержки, что необходимо добавить в письме, чтобы оно стало понятным.
    Отвечай так, как если бы ты лично общалась с клиентом. Будь вежливой, поздоровайся с ним, а потом укажи кратко по пунктам, чего не хватает. Не приводи примеры названий.

    Следуй инструкциям, отвечай кратко, но по делу. Думай дважды. Не сильно концетрируйся на контексте всего письма, только на название моделей. В ответе кроме json-файла ничего писать не нужно.

    Структура ответа:

    {{
    'flag': ...,
    'answer': ...,
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
            'body': body
        })
