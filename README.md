# Автоматическая диспетчеризация заявок

Запуск осуществлялся на Windows 11 (R5 5600, 32GB RAM, RTX 4060ti).

На вашем компьютере должен быть установлен docker desktop (можно скачать по ссылке https://www.docker.com/products/docker-desktop/).

0. Склонировать данный репозиторий
```
git clone https://github.com/ZotovNikita/dispatching-requests.git
```

1. Перейти в склонированную директорию
```powershell
cd dispatching-requests
```

2. Переименовать файл `.env.example` в `.env` и указать в нем свои пути `LOCAL_OLLAMA_MODELS` и `LOCAL_HUGGINGFACE_MODELS` для сохранения языковой модели, если хотите изменить пути по умолчанию

3. Собрать проект
```
docker build .
```

4. Запустить контейнеры
```
docker-compose up -d
```

5. Спуллить модель
```
docker exec -it ollama ollama pull gemma2:9b
```
Swagger: http://localhost:8910/docs

Frontend: http://localhost:8558/

Centrifugo: http://localhost:8822/

Выбор Ollama для проекта с использованием LLM Gemma 2 оправдан, так как этот инструмент требует меньше видеопамяти по сравнению с vLLM, что позволяет избежать нехватки ресурсов в условиях ограниченной инфраструктуры. Однако, для продакшн-среды лучше использовать vLLM, так как он обеспечивает более высокую производительность и оптимизацию работы с большими языковыми моделями, что критично для масштабируемых приложений.
