FROM postgres:alpine

COPY filtered_mini.sql /docker-entrypoint-initdb.d

RUN chmod a+r /docker-entrypoint-initdb.d/*

EXPOSE 6666

#docker run --rm --name mypgdb -v /home/client/Desktop/burnout_detection/postgres/pgdata:/var/lib/postgresql/data -e POSTGRES_PASSWORD=1234 -e POSTGRES_DB=burnout -p 6666:5432 mypostg