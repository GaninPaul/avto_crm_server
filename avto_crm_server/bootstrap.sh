#!/usr/bin/env bash
sh /home/avtomall/.atol/EoU/EthOverUsb.sh &
#python3 manage.py runserver 192.168.10.85:8000 &
celery worker -A avto_crm_server --loglevel=DEBUG > celery_debug.log &
