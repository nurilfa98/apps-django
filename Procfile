web: gunicorn apps_modular.wsgi --log-file - 
#or works good with external database
web: python manage.py migrate && gunicorn apps_modular.wsgi