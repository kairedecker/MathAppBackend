# MathAppBackend

Setup from: (Without gunicorn and nginx)
https://testdriven.io/blog/dockerizing-django-with-postgres-gunicorn-and-nginx/



Checkout this as well:
https://github.com/veryacademy/docker-mastery-with-django

```
docker-compose build
docker-compose run --rm app django-admin startproject core .
docker-compose up
```
or 
```
docker-compose up -d --build
```


Database migrations from Django on docker: (not necessary with etrypoint.sh!)
```
docker-compose exec web python manage.py migrate --noinput
```
