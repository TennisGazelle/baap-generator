FROM ubuntu:20.04

LABEL authors="Daniel Lopez <daniellopez@nevada.unr.edu>"

WORKDIR /app

RUN apt-get update -y 
RUN apt-get install -y python3 python3-dev python3-pip 

# Docker Cache Leverage
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT [ "python3" ]

CMD [ "main.py" ]