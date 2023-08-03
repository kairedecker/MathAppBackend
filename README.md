# MathAppBackend

Setup from: 
https://testdriven.io/blog/dockerizing-django-with-postgres-gunicorn-and-nginx/
Without gunicorn and nginx

Build and Run:
```
docker-compose up -d --build
```

Database migrations from Django on docker:
```
docker-compose exec web python manage.py migrate --noinput
```

