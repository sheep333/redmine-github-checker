FROM python:3.7

WORKDIR /var/www/
ADD . /var/www/

RUN pip install pipenv
RUN pip install -r requirements.txt

EXPOSE 8000
CMD ["python", "src/manage.py", "runserver", "0.0.0.0:8000"]
