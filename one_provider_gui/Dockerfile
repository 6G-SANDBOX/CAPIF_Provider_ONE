FROM python:3.8
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y jq && apt-get clean

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
ADD requirements.txt /usr/src/app/
RUN pip install -r requirements.txt

ADD . /usr/src/app/
RUN mkdir -p ./capif_ops/certs

EXPOSE 8085

CMD ["sh", "prepare.sh"]