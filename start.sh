python3 manage.py migrate
python3 manage.py collectstatic --noinput
gunicorn -w 4 smm_tools.wsgi:application -b 0.0.0.0:8000
