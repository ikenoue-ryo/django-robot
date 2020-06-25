#!/bin/sh

app=robot_project
while :
do
        if python /code/$app/manage.py migrate; then
                break
        else
                sleep 1
        fi
done
uwsgi --ini /code/$app/$app/uwsgi.ini

exit 0
