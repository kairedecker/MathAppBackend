# MathAppBackend

Setup from: (Without gunicorn and nginx)  
https://testdriven.io/blog/dockerizing-django-with-postgres-gunicorn-and-nginx/



Checkout this as well:  
https://github.com/veryacademy/docker-mastery-with-django  
With this tutorial on youtube:  
https://www.youtube.com/watch?v=W5Ov0H7E_o4&list=PLOLrQ9Pn6cazCfL7v4CdaykNoWMQymM_C&ab_channel=VeryAcademy  

Clone repo and start with setting up local python env:
```
python -m venv env
```
On Mac activate:
```
source env/bin/activate
```

On Windows activate (Git bash):
```
env/bin/activate
```

Then install requirements.txt: 
```
python -m pip install -r requirements.txt
```

Create .env.dev file -> Will hold secret keys and SQL user and password   

Then build docker image and create django project  
```
docker-compose build
docker-compose run --rm app django-admin startproject core .
docker-compose up
```

For mac add the following after building to update local file permissions:
```
chmod +x app/entrypoint.sh
```

For changes in models:
```
docker-compose run --rm app python manage.py makemigrations
docker-compose exec web python manage.py migrate --noinput
```

