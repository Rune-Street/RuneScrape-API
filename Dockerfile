FROM python:3.8.2-slim-buster


RUN pip3 install --upgrade pip

RUN adduser --disabled-password --gecos '' runescrape
WORKDIR /home/runescrape
USER runescrape

ENV PATH="/home/runescrape/.local/bin:${PATH}"
COPY --chown=runescrape:runescrape requirements.txt /tmp
RUN pip3 install --user -r /tmp/requirements.txt

COPY --chown=runescrape:runescrape .flaskenv .
COPY --chown=runescrape:runescrape runescrape_api runescrape_api
COPY --chown=runescrape:runescrape migrations migrations

CMD gunicorn -b 0.0.0.0:8080 --worker-class eventlet --worker-connections=1000 --workers=5  runescrape_api.wsgi:app
