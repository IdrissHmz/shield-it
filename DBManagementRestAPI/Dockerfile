# pull official base image
FROM ubuntu:20.04

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apt-get update && apt-get install -y python3.8 && apt-get install -y python3-pip && apt-get install -y netcat
RUN pip3 install --no-cache --upgrade pip setuptools


# install dependencies
RUN pip install --upgrade pip

COPY ./requirements.txt .

RUN pip install -r requirements.txt
RUN pip install djongo

# copy entrypoint.sh
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh


# copy project
COPY . .

# run entrypoint.sh
CMD ["./entrypoint.sh"]


# docker build -t dbmanagementrest .
# docker run -p 8080:8080 dbmanagementrest
