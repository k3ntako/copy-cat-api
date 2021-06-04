FROM  python:3.9.5

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

COPY ./requirements.txt /copycat/requirements.txt

WORKDIR /copycat

RUN pip install -r requirements.txt

ENV FLASK_APP=copycat
ENV FLASK_ENV=production
ENV APP_CONFIG=config.ProductionConfig

COPY . /copycat

RUN flask db upgrade

EXPOSE 5000

CMD [ "waitress-serve", "--port=5000", "--call", "copycat:create_app" ]

