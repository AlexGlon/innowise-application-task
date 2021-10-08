FROM python:3.9.6

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get -y install libpq-dev
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*

ADD . /opt/support_desk/
COPY entrypoint.sh /opt/support_desk/entrypoint.sh
WORKDIR opt/support_desk/

RUN pip install --upgrade pip
#RUN pip install psycopg2-binary
RUN pip install -r requirements.txt --no-cache-dir

ENTRYPOINT [ "/bin/bash", "/opt/support_desk/entrypoint.sh" ]