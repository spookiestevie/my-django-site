# my-django-site

1. cd Desktop/my-django-site
2. source venv/bin/activate
3. python manage.py runserver
4. http://127.0.0.1:8000/test2

su postgres
psql
create database rise;
create user rise with password '[password]';
alter database rise owner rise;

ctrl d

python manage.py makemigrations
python manage.py migrate

check settings.py file and adjust postgres settings

su postgres
psql
\c rise
\dt+
select count (*) rise from blog_lastblocks;
