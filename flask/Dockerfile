FROM python:3.11

WORKDIR /app

COPY requirements.txt requirements.txt

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["flask", "--app", "ecdc", "init-db"]
CMD ["waitress-serve", "--listen=0.0.0.0:5000", "--call", "ecdc:create_app"]
EXPOSE 5000
