FROM python:3.14

WORKDIR /app

COPY requirements.txt req.txt

RUN pip install -r req.txt

COPY . .

EXPOSE 8080

CMD ["python", "app.py"]