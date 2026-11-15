FROM python:3.12-slim

RUN pip install --no-cache-dir requests
WORKDIR /app
ENV PYTHONUNBUFFERED=1

CMD ["python", "src/collecter_velib.py"]
