@echo off

call activatevenv.bat

pip install -r req.txt

python manage.py runserver
