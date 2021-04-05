FROM python:3.9-slim

ENV INSTALL_PATH /web_messaging
RUN mkdir -p $INSTALL_PATH

WORKDIR $INSTALL_PATH

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD gunicorn -b 0.0.0.0:8080 --access-logfile - "web_messaging.app:create_app()"