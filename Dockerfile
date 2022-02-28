FROM python:3.6

MAINTAINER Kym Eden

RUN apt-get update

ADD requirements.txt /opt/wallapocket/
RUN pip3 install -r /opt/wallapocket/requirements.txt

ADD src /opt/wallapocket/src

ENTRYPOINT ["/opt/wallapocket/src/main.py"]
CMD []
