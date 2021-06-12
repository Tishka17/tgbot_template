FROM python:3.9-slim

WORKDIR /usr/src/app/bot_name

COPY requirements.txt /usr/src/app/bot_name
RUN pip install -r /usr/src/app/bot_name/requirements.txt
COPY . /usr/src/app/bot_name

CMD python3 /usr/src/app/bot_name/bot.py
