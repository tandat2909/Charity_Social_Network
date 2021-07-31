backup database
python manage.py dumpdata -o Data/stt_ddMMYYYY.json

update database:
python manage.oy loaddata Data/stt_ddMMYYYY.json