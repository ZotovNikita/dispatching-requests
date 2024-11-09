# dispatching-requests

0. Склонировать данный репозиторий
```
git clone https://github.com/ZotovNikita/dispatching-requests.git
```

1. Перейти в склонированную директорию
```
cd dispatching-requests
```

2. Переименовать файл `.env.example` в `.env`

3. Собрать проект
```
docker compose build
```

4. Запустить контейнеры
```
docker compose up -d
```

5. Спуллить модель
```
docker exec -it ollama ollama pull gemma2:9b
```
