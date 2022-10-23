FROM ubuntu:20.04


WORKDIR /app

ENV PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install python3.7 && apt-get install python3-pip -y && apt-get install -y netcat
RUN pip3 install --no-cache --upgrade pip setuptools

COPY requirementsbis.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
RUN python3 -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'), nltk.download('wordnet')"

#RUN mkdir data

RUN chmod +x main_script.sh

CMD [ "sh", "./main_script.sh"]