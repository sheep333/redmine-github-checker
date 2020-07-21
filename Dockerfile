FROM python:3.7

ARG dir

RUN mkdir -p ${dir}

WORKDIR /var/www/
ADD . /var/www/
# リポジトリ外のフォルダはマウントできない
ADD ${dir} ${dir}

RUN pip install pipenv
RUN pip install -r requirements.txt
