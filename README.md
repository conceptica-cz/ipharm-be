
# iPharm backend app

## Installation and run

**Requirements:**

You need `docker` and `docker-compose` to run the app.

**Clone repo:**

```shell
git clone https://github.com/conceptica-cz/ipharm-be.git
```

**Add environment variables files:**

The application uses multiple environment files. You have to create them and add set variables.
See the **Environment Variables** [section](#environment-variables) below.

You have also to set variables for reference (iciselniky) app. 
See the **Environment Variables** section of reference app's
[README](https://github.com/conceptica-cz/iciselniky-be#environment-variables).

**Run app locally:**

```shell
cd ipharm-be
docker-compose -f docker-compose.yml up -d
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

## Environment variables

Environment variables are used to configure the docker services. 
They are set in files `./.envs/.development/.ipharm_app`, `./.envs/.development/.ipharm_postgres` 
and `./.envs/.development/.ipharm_redis`.

### App variables (`./.envs/.development/.ipharm_app`)

Django application variables. Used by `ipharm-app`, `ipharm-worker`, `ipharm-beat`  docker service.

`SECRET_KEY` - (must be set) django secret key.

`ALLOWED_HOSTS` - (must be set) django `ALLOWED_HOSTS` - list of hosts separated by comma (or just `*`).

`BASE_IPHARM_REFERENCES_URL` - (default is `http://iciselniky-app:8000/api/v1`) base references API (iciselniky app) url.

`IPHARM_REFERENCES_TOKEN` - (must be set) references API (iciselniky app) token.

`BASE_REFERENCES_URL` - (must be set) external API (patient) url.

`REFERENCES_TOKEN` - (must be set) external API (patient) token.


`DEBUG` - (default is `False`) django `DEBUG` variable.

`ENVIRONMENT` - (default is `production`) Sentry environment.

`LOG_LEVEL` - (default is `"INFO"`) logging level.

### Postgres variables (`./.envs/.development/.ipharm_postgres`)

Postgres variables. Used by `ipharm-postgres` and also by `ipharm-app`, `ipharm-worker`, 
`ipharm-beat` docker services.

`POSTGRES_HOST` - (must be set) postgres host.

`POSTGRES_PORT` - (must be set) postgres port.

`POSTGRES_DB` - (must be set) postgres database name.

`POSTGRES_USER` - (must be set) postgres user.

`POSTGRES_PASSWORD` - (must be set) postgres password.

### Redis variables (`./.envs/.development/.ipharm_redis`)

Redis variables. Used by `ipharm-redis` and also by `ipharm-app`, `ipharm-worker`, `ipharm-beat`, 
`ipharm-flower` docker services.

`REDIS_HOST` - (must be set) redis host.

`REDIS_PORT` - (must be set) redis port.

`CELERY_BROKER_URL` - (must be set) broker set. Used by flower.


## REST API

OpenAPI UI: `/api/v1/schema/`

Swagger scheme: `/api/v1/schema/swagger-ui/`
