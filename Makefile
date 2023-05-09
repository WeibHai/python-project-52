start:
	poetry run gunicorn --workers=5 task_manager.wsgi

start-dev:
	python manage.py runserver
