migrate:
	python manage.py makemigrations --settings=ogame_forum_api.settings.${ENV_REF}
	python manage.py migrate --settings=ogame_forum_api.settings.${ENV_REF}

shell:
	python manage.py shell --settings=ogame_forum_api.settings.${ENV_REF}


run:
	python manage.py runserver 0.0.0.0:9099 --settings=ogame_forum_api.settings.${ENV_REF}
