FROM python:3.8.2-slim-buster

RUN adduser --disabled-password --gecos '' runescrape
WORKDIR /home/runescrape
USER runescrape

COPY requirements.txt /tmp
RUN pip3 install --no-warn-script-location -r /tmp/requirements.txt

COPY runescrape_api .

CMD gunicorn -b 0.0.0.0:8000 runescrape_api.wsgi:app
