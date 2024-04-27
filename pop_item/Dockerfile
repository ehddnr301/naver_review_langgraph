FROM python:3.8-slim

WORKDIR /app

RUN pip install redis

COPY poper.py /app

CMD ["python", "poper.py"]