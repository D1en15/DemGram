# DemGram
Easy Django Task Manager

# Settings:
task_manager/settings.py

# Commands to run
redis-server
celery -A task_manager worker -l INFO
celery -A task_manager beat -l INFO
python manage.py runserver
