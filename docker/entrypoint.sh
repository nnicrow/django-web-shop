#!/bin/sh
echo Start app
cd backend/
echo Wait 5 seconds to run dependents
sleep 5
echo Run migrate
python manage.py migrate
echo Create user ${SUPERUSER} with email ${SUPERUSER_EMAIL} and password ${SUPERUSER_PASSWORD}
python manage.py create_superuser_with_password --noinput --username ${SUPERUSER} --email ${SUPERUSER_EMAIL} --password ${SUPERUSER_PASSWORD} --preserve
echo Run server
python manage.py runserver 0.0.0.0:8000
