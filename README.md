# iPharm backend app

## Installation and run

**Requirements:**

You need `docker` and `docker-compose` to run the app.

**Clone repo:**

```shell
git clone https://github.com/conceptica-cz/ipharm-be.git
```

**Add environment variables files:**

The application uses multiple environment files.

1) create two files `.ipharm_postgres` and `.ipharm_app` in directory `./.envs/.development/`:
```shell
./.envs/.development/.ipharm_app
./.envs/.development/.ipharm_postgres
```
2) Add to .app variable(s):
```shell
SECRET_KEY=...
DEBUG=True
```

3) Add to .postgres variable(s):
```shell
POSTGRES_HOST=ipharm_postgres
POSTGRES_PORT=...
POSTGRES_DB=...
POSTGRES_USER=...
POSTGRES_PASSWORD=...
```

**Run app locally:**

```shell
cd ipharm-be
docker-compose -f docker-compose.development.yml up -d
```

**Populate database with fake data and create superuser (you need to do it only once):**

```shell
 docker-compose exec app python manage.py populate
 docker-compose exec app python manage.py createsuperuser
```

Now app is running. Check http://localhost:8000
Use superuser credentials to add some user.


**Stop app and remove containers:**

```shell
docker-compose down
```

## REST API

OpenAPI scheme: `/api/v1/schema/`
Swagger scheme: `/api/v1/schema/swagger-ui/`