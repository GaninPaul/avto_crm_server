#!/usr/bin/bash

. venv/bin/activate
./manage.py runserver & celery worker -A avto_crm_server --logging=DEBUG > celery_debu.log
