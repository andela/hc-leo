web: gunicorn hc.wsgi && ./manage.py ensuretriggers && ./manage.py sendalerts && ./manage.py sendreports
migrate: ./manage.py migrate
triggers: ./manage.py ensuretriggers
superuser: ./manage.py createsuperuser
