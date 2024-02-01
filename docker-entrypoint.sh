#!/bin/sh

flask db upgrade

#exec gunicorn --bind 0.0.0.0:80 "app:create_app()"
# exec gunicorn --bind 0.0.0.0:5000 "app:create_app()"
# exec flask run --host 0.0.0.0
if [ "$ENV" = "local" ]
then
    exec flask run --host 0.0.0.0
else
    exec gunicorn --bind 0.0.0.0:5000 "app:create_app()"
fi