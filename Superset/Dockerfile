FROM apache/superset:latest

USER root

RUN apt-get update && apt-get install -y \
    vim \
    && rm -rf /var/lib/apt/lists/*

# RUN echo 'nameserver 8.8.8.8' >> /etc/resolv.conf


RUN pip install mysqlclient 

COPY sqlalchemy_mongobi-0.2.1-py3-none-any.whl .

RUN pip install ./sqlalchemy_mongobi-0.2.1-py3-none-any.whl

COPY entrypoint.sh /
RUN chmod a+x /entrypoint.sh

USER superset

ENV LIBMYSQL_ENABLE_CLEARTEXT_PLUGIN=1

ENTRYPOINT ["/entrypoint.sh"]