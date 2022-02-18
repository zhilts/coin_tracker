FROM python:3-alpine

WORKDIR /app
ADD requirements.txt /app/
RUN pip install -r requirements.txt
ADD . /app/

ENTRYPOINT ["python"]

CMD ["./telegram_bot.py"]