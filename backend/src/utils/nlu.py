import joblib

import pandas as pd
import torch
import onnxruntime as ort
from transformers import AutoTokenizer, AutoModel
from sklearn.preprocessing import LabelEncoder

from .ner import get_one_serial_number


tokenizer = AutoTokenizer.from_pretrained('intfloat/multilingual-e5-large-instruct')
model_embedding = AutoModel.from_pretrained('intfloat/multilingual-e5-large-instruct')
model_classification_equipment_type = joblib.load('./models/cb_equipment_model.pkl')

label_encoder: LabelEncoder = joblib.load('./models/label_encoder.pkl')
model_classification_failure_point = ort.InferenceSession('./models/best_model.onnx', providers=['CPUExecutionProvider'])


def average_pool(last_hidden_states: torch.Tensor, attention_mask: torch.Tensor) -> torch.Tensor:
    ''' 
    Функция average_pool выполняет усреднение скрытых состояний последнего слоя модели, 
    учитывая маску внимания. 

    Параметры:
    - last_hidden_states: Тензор, содержащий скрытые состояния последнего слоя модели. 
      Размерность тензора - (batch_size, sequence_length, hidden_size).
    - attention_mask: Тензор, указывающий, какие токены следует учитывать при усреднении. 
      Размерность тензора - (batch_size, sequence_length).

    Возвращает:
    - Тензор, представляющий усредненные эмбеддинги для каждого примера в батче. 
      Размерность тензора - (batch_size, hidden_size).
    
    Процесс:
    1. Скрытые состояния, соответствующие токенам, которые не должны учитываться (например, паддинг), 
       заменяются на нули с помощью метода masked_fill.
    2. Затем выполняется суммирование скрытых состояний по временной оси (dim=1).
    3. Наконец, результат делится на количество токенов, которые были учтены (сумма маски внимания), 
       чтобы получить усредненные эмбеддинги.
    '''
    last_hidden = last_hidden_states.masked_fill(~attention_mask[..., None].bool(), 0.0)
    return last_hidden.sum(dim=1) / attention_mask.sum(dim=1)[..., None]


def create_embeddings(topic: str, description: str, model, tokenizer) -> torch.Tensor:
    text_input = f"{topic} {description}"

    batch_dict = tokenizer([text_input], max_length=512, padding=True, truncation=True, return_tensors='pt')

    with torch.no_grad():
        outputs = model(**batch_dict)

    embeddings = average_pool(outputs.last_hidden_state, batch_dict['attention_mask'])
    embeddings = torch.nn.functional.normalize(embeddings, p=2, dim=1)

    return embeddings


def generate_prediction_equipment_type(topic: str, description: str, model, tokenizer, cb_model) -> str:
    ''' 
    Функция generate_prediction генерирует предсказание темы обращения для заданного текста, 
    состоящего из темы и описания, используя предобученную модель и токенизатор.

    Параметры:
    - topic: Строка, представляющая тему текста, для которого необходимо сделать предсказание.
    - description: Строка, представляющая описание текста, для которого необходимо сделать предсказание.
    - model: Предобученная модель, используемая для получения эмбеддингов текста.
    - tokenizer: Токенизатор, используемый для преобразования текста в формат, 
      подходящий для модели.
    - cb_model: Модель, используемая для генерации предсказаний на основе эмбеддингов.

    Возвращает:
    - str: Предсказанный тип обращения для заданного текста.

    Процесс:
    1. Формируется текстовый ввод, объединяя тему и описание.
    2. Текст токенизируется и преобразуется в тензоры, подходящие для модели, с учетом 
       максимальной длины, паддинга и обрезки.
    3. С помощью модели получаются скрытые состояния, при этом отключается градиент 
       для экономии памяти и ускорения вычислений.
    4. Вызывается функция average_pool для получения усредненных эмбеддингов на основе 
       скрытых состояний и маски внимания.
    5. Эмбеддинги нормализуются для улучшения качества предсказаний.
    6. На основе нормализованных эмбеддингов генерируется предсказание с помощью cb_model.
    7. Возвращается предсказанный класс.
    '''

    embeddings = create_embeddings(topic, description, model, tokenizer)

    prediction = cb_model.predict(embeddings.numpy())

    return str(prediction[0][0])


def generate_predictions_from_dataframe(df: pd.DataFrame, model_embedding, tokenizer, cb_model, model_onnx: ort.InferenceSession, label_encoder) -> pd.DataFrame:
    ''' 
    Функция generate_predictions_from_dataframe генерирует предсказания для каждого 
    текста в DataFrame, используя предобученную модель и токенизатор.

    Параметры:
    - df: DataFrame, содержащий данные с текстами, для которых необходимо сделать предсказания. 
      Ожидается, что в DataFrame есть столбцы 'Тема' и 'Описание'.
    - model: Предобученная модель, используемая для получения эмбеддингов текста.
    - tokenizer: Токенизатор, используемый для преобразования текстов в формат, 
      подходящий для модели.
    - cb_model: Модель, используемая для генерации предсказаний на основе эмбеддингов.

    Возвращает:
    - pd.DataFrame: Датафрейм с предсказанными классами для каждого текста в DataFrame.

    Процесс:
    1. Инициализируется пустой список для хранения предсказаний.
    2. Для каждой строки в DataFrame:
       - Формируется текстовый ввод, объединяя 'Тема' и 'Описание'.
       - Текст токенизируется и преобразуется в тензоры, подходящие для модели.
       - С помощью модели получаются скрытые состояния.
       - Вызывается функция average_pool для получения усредненных эмбеддингов.
       - Эмбеддинги нормализуются.
       - На основе нормализованных эмбеддингов генерируется предсказание с помощью cb_model.
       - Предсказание добавляется в список.
    3. Возвращается датафрейм с предсказанными классами.
    '''
    predictions = []

    for _, row in df.iterrows():
        embeddings = create_embeddings(row['Тема'], row['Описание'], model_embedding, tokenizer)

        prediction_cls1 = cb_model.predict(embeddings.numpy())
        prediction_cls1 = prediction_cls1[0][0]

        outputs = model_onnx.run(None, {'input': embeddings.reshape(1, 1, -1).numpy()})
        pred = outputs[0].argmax(axis=1)
        prediction_cls2 = label_encoder.inverse_transform(pred)
        prediction_cls2 = prediction_cls2.item()

        prediction_cls3 = get_one_serial_number(row['Тема'], row['Описание'])

        predictions.append((prediction_cls1, prediction_cls2, prediction_cls3))

    return pd.DataFrame(predictions, columns=['Тип оборудования', 'Точка отказа', 'Серийный номер'])


def generate_prediction_failure_point(topic: str, description: str, model_embedding, tokenizer, model_onnx: ort.InferenceSession, label_encoder) -> str:
    embeddings = create_embeddings(topic, description, model_embedding, tokenizer)

    outputs = model_onnx.run(None, {'input': embeddings.reshape(1, 1, -1).numpy()})
    pred = outputs[0].argmax(axis=1)

    cls = label_encoder.inverse_transform(pred)

    return cls.item()
