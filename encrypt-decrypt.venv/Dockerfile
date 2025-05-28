FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt requirements.txt

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt
RUN flask --app ecdc init-db

ENV PORT=5000

EXPOSE 5000
CMD ["python", "app.py"]
