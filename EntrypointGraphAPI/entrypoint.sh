#!/bin/sh

if [ "$MANGODATABASE" = "shield_db" ]
then
    echo "Waiting for MongoDB..."

    while ! nc -z $NOSQL_HOST $NOSQL_PORT; do
      sleep 0.1
      echo "waiting ..."
    done

    echo "MongoDB started"
fi

#python3 manage.py flush --no-input

python3 manage.py migrate
python3 manage.py runserver 0.0.0.0:8000
echo "Server is running "
#exec "$@"
