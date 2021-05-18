
migration:
	-rm db.sqlite3
	-rm -rv core/migrations/00*
	python manage.py makemigrations
	python manage.py migrate
	python manage.py createsuperuser
	-python manage.py loaddata datadump.json
	python manage.py runserver


datadump:
	python manage.py dumpdata core auth --indent 2 > datadump.json

