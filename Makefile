start:
	poetry run gunicorn --workers=5 task_manager.wsgi

start-dev:
	poetry manage.py runserver
	
mmigrate:
	python3 manage.py makemigrations
	
migrate:
	python3 manage.py migrate
	
test:
	poetry run python3 manage.py test

