# MathAppBackend

Setup from: 
https://testdriven.io/blog/dockerizing-django-with-postgres-gunicorn-and-nginx/
Without gunicorn and nginx

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

