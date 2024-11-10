import re
import typing as t
from itertools import chain


_DEFAULT_PATTERNS = [
    r'\b[A-Za-zА-Яа-я]{1,4}\d{7,14}\b(?:\([^\)]*\))?',
]


def russian_to_english(text: str) -> str:
    """переводит русские символы в английские, схожие по начертанию

    Args:
        text (str): Входной текст для преобразования

    Returns:
        str: Результат преобразования
    """
    russian = "СМТВАРОКЕНХ"
    english = "CMTBAPOKEHX"
    translation_table = str.maketrans(russian, english)
    return text.translate(translation_table)


def id_preprocessing(id: str) -> str:
    """Переводит Серийный номер в канонический вид (Английские буквы + верхний регистр)

    Args:
        id (str): Исходный серийный номер

    Returns:
        str: Серийный номер в каноническом виде
    """
    return russian_to_english(id.upper())


def get_all_serial_numbers(
    header: str,
    body: str,
    patterns: t.Iterable[str] | None = None,
    preprocessing: t.Callable[[str], str] = lambda s: s,
    default_value: str = 'Уточнить',
) -> list[str]:
    """Возвращает все найденные Серийные номера в тексте заголовка письма и его тела

    Args:
        header (str): Заголовок письма
        body (str): Тело письма
        patterns (t.Iterable[str], optional): Признаки кластеров Серийных номеров. Defaults to _DEFAULT_PATTERNS
        preprocessing (t.Callable[[str], str], optional): Функция по предобработке результирующих Серийных номеров. Defaults to (lambda s: s)
        default_value (str, optional): Значение, которое буде возвращено, если Серийные номера не будут найдены. Defaults to Уточнить

    Returns:
        list[str]: Список всех найденных Серийных номеров в письме
    """
    if patterns is None:
        patterns = _DEFAULT_PATTERNS

    res = list(
        map(
            preprocessing,
            chain(*(
                set(re.findall(pattern, header) + re.findall(pattern, body))
                for pattern in patterns
            ))
        )
    )

    if res:
        return res

    return [default_value]


def get_one_serial_number(
    header: str,
    body: str,
    patterns: t.Iterable[str] | None = None,
    preprocessing: t.Callable[[str], str] = lambda s: s,
    default_value: str = 'Уточнить',
) -> str:
    """Возвращает первое вхождение Серийного номера в тексте заголовка письма и его тела

    Args:
        header (str): Заголовок письма
        body (str): Тело письма
        patterns (t.Iterable[str], optional): Признаки кластеров Серийных номеров. Defaults to _DEFAULT_PATTERNS
        preprocessing (t.Callable[[str], str], optional): Функция по предобработке результирующих Серийных номеров. Defaults to (lambda s: s)
        default_value (str, optional): Значение, которое буде возвращено, если Серийные номера не будут найдены. Defaults to Уточнить

    Returns:
        str: Первое вхождение Серийного номера в письме
    """
    if patterns is None:
        patterns = _DEFAULT_PATTERNS

    agg_pattern = '|'.join(patterns)
    res = re.findall(agg_pattern, ' '.join((header, body)))

    if res:
        return preprocessing(res[0])

    return default_value
