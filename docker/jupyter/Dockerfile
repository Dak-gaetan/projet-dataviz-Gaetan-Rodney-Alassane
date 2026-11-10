FROM python:3.12-slim

RUN pip install --no-cache-dir requests
WORKDIR /app
ENV PYTHONUNBUFFERED=1

# Le code (src/) et les données (data/) sont montés depuis le dépôt par docker-compose
CMD ["python", "src/collecter_velib.py"]
