# iPharm backed app

## Installation and run

Requirements:

You need `docker` and `docker-compose` to run the app.

Clone repo:

```shell
git clone https://github.com/conceptica-cz/ipharm-be.git
```

Run app locally:

```shell
cd ipharm-be
docker-compose -f docker-compose.local.yml up -d
```

Populate database with fake data and create superuser (you need to do it only once):

```shell
 docker-compose exec app python manage.py populate
 docker-compose exec app python manage.py createsuperuser
```

Now app is running. Check http://localhost:8000
Use superuser credentials to add some user.


Stop app and remove containers:

```shell
docker-compose down
```

Build app image:

```shell
docker-compose build app
```