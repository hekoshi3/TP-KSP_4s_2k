@echo off

cd .. & cd .venv/Scripts/ & activate & cd .. & cd .. & cd myproject
py -3 manage.py runserver
