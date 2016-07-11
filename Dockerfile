FROM python:2.7.12

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install -v -r requirements.txt

WORKDIR analyse_url
CMD ["nameko","run","analyse_url"]
