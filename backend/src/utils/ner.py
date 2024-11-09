import itertools
import re
import typing as t


_patterns = [
    r'\b[A-Za-zА-Яа-я]\d{9}\b(?:\([^\)]*\))?',
    r'\b[A-Za-zА-Яа-я]{3}\d{11}\b(?:\([^\)]*\))?',
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


def get_all_serial_numbers(header: str, body: str, patterns: t.List[str] = None, preprocessing: t.Callable[[str], str] = lambda s: s, default_value: str = 'Уточнить') -> t.List[str]:
    """Возвращает все найденные Серийные номера в тексте заголовка письма и его тела

    Args:
        header (str): Заголовок письма
        body (str): Тело письма
        patterns (t.List[str]): Признаки кластеров Серийных номеров
        preprocessing (_type_, optional): Функция по предобработке результирующих Серийных номеров. Defaults to lambdas:s.

    Returns:
        t.List[str]: Список всех найденных Серийных номеров в письме
    """
    if patterns is None:
        patterns = _patterns

    res = list(
        map(
            lambda s: preprocessing(s),
            itertools.chain(*[
                set(re.findall(pattern, header) + re.findall(pattern, body))
                for pattern in patterns
            ])
        )
    )
    if res:
        return res
    return [default_value]


def get_one_serial_number(header: str, body: str, patterns: t.List[str] = None, preprocessing: t.Callable[[str], str] = lambda s: s, default_value: str = 'Уточнить') -> str:
    """Возвращает первое вхождение Серийного номера в тексте заголовка письма и его тела

    Args:
        header (str): Заголовок письма
        body (str): Тело письма
        patterns (t.List[str]): Признаки кластеров Серийных номеров
        preprocessing (_type_, optional): Функция по предобработке результирующих Серийных номеров. Defaults to lambdas:s.

    Returns:
        t.List[str]: Первое вхождение Серийного номера в письме
    """
    if patterns is None:
        patterns = _patterns

    agg_pattern = '|'.join(patterns)
    res = re.findall(agg_pattern, ' '.join((header, body)))
    if res:
        return preprocessing(res[0])
    return default_value
