python manage.py makemigrations || exit 1
python manage.py migrate || exit 1
exec python manage.py runserver 0.0.0.0:8000
