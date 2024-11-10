# dispatching-requests

Запуск осуществлялся с Windows 11 (R5 5600, 32GB RAM, RTX 4060ti).

0. Склонировать данный репозиторий
```
git clone https://github.com/ZotovNikita/dispatching-requests.git
```

1. Перейти в склонированную директорию
```powershell
cd dispatching-requests
```

2. Переименовать файл `.env.example` в `.env`

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
