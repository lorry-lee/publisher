@echo off
TASKKILL /F /IM python.exe
python manage.py runserver 0.0.0.0:8000
