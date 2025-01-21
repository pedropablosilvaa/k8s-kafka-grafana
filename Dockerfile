FROM python:3.9.6

LABEL Maintainer="Pedro Pablo Silva"

RUN mkdir /usr/src/app

COPY src /usr/src/app
COPY requirements.txt /usr/src/app

WORKDIR /usr/src/app

RUN pip3 install -r requirements.txt

CMD [ "python3", "main.py" ]
#docker build -t myapp .
#docker run -d --name myapp-container myapp
