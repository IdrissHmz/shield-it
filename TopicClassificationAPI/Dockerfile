FROM ubuntu:20.04


WORKDIR /app

ENV PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install -y python3.8 && apt-get install python3-pip -y && apt-get install -y netcat
RUN pip3 install --no-cache --upgrade pip setuptools

COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
#RUN python3 -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'), nltk.download('wordnet')"

RUN pip install typing-extensions --upgrade
#RUN mkdir data


CMD [ "uvicorn","main:app","--reload","--host", "0.0.0.0", "--port", "81"]