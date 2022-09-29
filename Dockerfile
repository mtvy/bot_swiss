FROM python:latest

WORKDIR /app

COPY . .

RUN pip3 install -r server_configs/requirements.txt

CMD ["python", "bot.py"]
