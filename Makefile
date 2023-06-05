start:
	poetry run gunicorn --workers=5 task_manager.wsgi

start-dev:
	poetry manage.py runserver
	
mmigrate:
	python3 manage.py makemigrations
	
migrate:
	python3 manage.py migrate

lint:
	poetry run flake8
	
test:
	poetry run python3 manage.py test

trans:
	django-admin compilemessages

tests-cov:
	poetry run coverage run ./manage.py test
	poetry run coverage xml

setup:
	poetry install
	poetry run python3 manage.py makemigrations
	poetry run python3 manage.py migrate
	poetry run gunicorn --bind 0.0.0.0:$(PORT) task_manager.wsgi

