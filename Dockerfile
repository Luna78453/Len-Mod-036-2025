FROM python:3.11-slim

WORKDIR /encryption-decryption.venv/ecdc

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

copy . .

EXPOSE 5000
CMD ['python', 'app.py']
