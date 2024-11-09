FROM python:3.12.5-slim-bookworm

RUN apt-get update && \
    apt-get install -y python3 python3-pip

WORKDIR /backend

COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r ./requirements.txt

COPY ./backend .

CMD ["python3", "-m", "src"]
