FROM python:3.7

WORKDIR /var/www/
ADD . /var/www/

RUN pip install pipenv
RUN pip install -r requirements.txt
