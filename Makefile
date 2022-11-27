migrate:
	python manage.py makemigrations
	python manage.py migrate

shell:
	python manage.py shell


run:
	python manage.py runserver 0.0.0.0:9099
