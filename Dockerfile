FROM python:3.12.3-slim as build

WORKDIR /src

COPY Pipfile .
COPY Pipfile.lock .

RUN pip3 install --upgrade pipenv
RUN pipenv requirements > /src/requirements.txt


FROM python:3.12.3-slim

ARG APP_VERSION
ENV APP_VERSION=$APP_VERSION
ENV GUNICORN_PORT 8080

WORKDIR /app

COPY --from=build /src/requirements.txt ./requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r ./requirements.txt

COPY static /app/static
COPY templates /app/templates
COPY *.py /app
COPY config.toml /app
COPY log.conf /app
EXPOSE $GUNICORN_PORT

CMD ["gunicorn", "--config", "gunicorn.conf.py", "--log-config", "log.conf" ]
