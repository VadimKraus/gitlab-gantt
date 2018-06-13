FROM docker.io/python:3.6
MAINTAINER Kuzon Chen <kuzoncby@gmail.com>

WORKDIR /opt
ENV HOME /opt
ENV LOGNAME=1001
ENV USER=1001
ADD . /opt/

RUN pip3 install -r requirements.txt \
    && rm -rf assets

EXPOSE 5000

ENTRYPOINT ["gunicorn"]
CMD ["application:app"]
