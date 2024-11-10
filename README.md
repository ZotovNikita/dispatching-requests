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

Frontend: http://localhost:8558/

Centrifugo: http://localhost:8822/
