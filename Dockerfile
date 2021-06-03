FROM  python:3.9.5

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

COPY ./requirements.txt /copycat/requirements.txt

WORKDIR /copycat

RUN pip install -r requirements.txt

ENV FLASK_APP=copycat
ENV FLASK_ENV=development

COPY . /copycat

EXPOSE 5000

CMD [ "flask", "run", "--host=0.0.0.0" ]
