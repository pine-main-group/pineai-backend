web: gunicorn burst.wsgi --log-file -
#or works good with external database
web: python manage.py migrate && gunicorn burst.wsgi
