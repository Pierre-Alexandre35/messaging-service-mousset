FROM python:3.7.5-slim-buster


WORKDIR /project
ADD . /project
RUN pip install -r requirements.txt
RUN pip install flask_login 
CMD ["python","app.py"]