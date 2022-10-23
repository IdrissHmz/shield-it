#!/bin/bash

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

year="1979" 
start_time="12"
off_time="17"
python3 -u main.py --year ${year} --start-time ${start_time} --off-time ${off_time}

# python -u main_3.py --year ${year} --month ${month}
