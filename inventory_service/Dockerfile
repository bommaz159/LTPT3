FROM python:3.9-slim

WORKDIR /app

COPY main.py .
COPY Controllers ./Controllers
COPY Entities ./Entities
COPY Infrastructure ./Infrastructure
COPY UseCases ./UseCases
COPY requirements.txt .

RUN pip install -r requirements.txt

CMD ["python", "main.py"]
