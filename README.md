# iPharm backend app

## Requirements

You need `docker` and `docker-compose` to run the app.

## Installation and configuration

### Clone the repository

```
$ git clone https://github.com/conceptica-cz/ipharm-be.git
$ cd ipharm-be
```

### Add iCiselniky environment variable files

The app depends on the [iCiselniky app](https://github.com/conceptica-cz/iciselniky-be).

Create a environment variable files for iCiselniky app:

- `./.envs/.development/.iciselniky_app`
- `./.envs/.development/.iciselniky_postgres`
- `./.envs/.development/.iciselniky_redis`

See the [iCiselniky app](https://github.com/conceptica-cz/iciselniky-be) for more information about variables.

### Run iCiselniky app

```
$ docker-compose up -d iciselniky-app
```

### Create iCiselniky superuser

```
$ docker-compose exec iciselniky-app python manage.py createsuperuser
```

Now you can login to the iCiselniky app's admin on http://localhost:8001/admin/

### Populate iCiselniky database with fake data (optional, development only)

```
$ docker-compose exec iciselniky-app python manage.py populate
```

### Add `ipharm` user and token to iCiselniky

To use [iCiselniky](https://github.com/conceptica-cz/iciselniky-be) API you have to get a token.

Create user and token:

```
$ docker-compose exec iciselniky-app python manage.py create_app_users
```

The command creates application users and tokens. The response shows the token for the `ipharm` user.

Note: you can also find the token in the [iCiselniky admin](http://localhost:8001/admin/authtoken/tokenproxy/) .

You have to add the `ipharm` token to the `.envs/.development/.ipharm_app` file (`ICISELNIKY_TOKEN` variable).

### Add environment variable files

Create a environment variable files for:

- `./.envs/.development/.ipharm_app`
- `./.envs/.development/.ipharm_postgres`
- `./.envs/.development/.ipharm_redis`

In the files, set environment variables, mainly those that do not have default values.

See the {ref}`Environment variables` section below for more information about variables.

### Run the app

```
$ cd ipharm-be
$ docker-compose up -d
```

### Create superuser

```
$ docker-compose exec ipharm-app python manage.py createsuperuser
```

Now you can login to the app's admin on localhost:8000/admin/

### Populate database with fake data (optional, development only)

```
$ docker-compose exec ipharm-app python manage.py populate
```

## Documentation

The documentation is available in the source code in the `/docs/build` directory

## Environment variables

### iPharm variables

File: `./.envs/.development/.izadanky_app`

Django application variables. Used by `izadanky-app`, `izadanky-worker-high-priority`, `izadanky-worker-low-priority`
, `izadanky-beat`  docker services.

#### ALLOWED_HOSTS

No default value (must be set).

Django `ALLOWED_HOSTS` - list of hosts separated by comma (or just `*`).

#### BASE_ICISELNIKY_URL

Default: `http://iciselniky-app:8000/api/v1`

Base iCiselniky API url.

#### ICISELNIKY_TOKEN

Default: emtpy value.

iCiselniky API token.

#### BASE_UNIS_URL

Default: emtpy value.

Base UNIS API (patient API) url.

#### UNIS_TOKEN

Default: emtpy value.

Unis API (patient API) token.

#### DEBUG

Default: `False`

#### ENVIRONMENT

Default: `production`

App's environment.

#### LOG_LEVEL

Default: `INFO`

Logging level.

#### SECRET_KEY

No default value (must be set).

Django secret key.

### Postgres variables

File: `./.envs/.development/.izadanky_postgres`

Postgres variables. Used by `izadanky-postgres` and also by `izadanky-app`, `izadanky-worker`, `izadanky-beat` docker
services.

#### POSTGRES_DB

No default value (must be set).

Postgres database name.

#### POSTGRES_PASSWORD

No default value (must be set).

Postgres database password.

#### POSTGRES_HOST

No default value (must be set).

Postgres database host.

#### POSTGRES_PORT

No default value (must be set).

Postgres database port.

#### POSTGRES_USER

No default value (must be set).

Postrgres database user.

### Redis variables

Redis variables. Used by `izadanky-redis` and also by `izadanky-app`, `izadanky-worker`, `izadanky-beat`
, `izadanky-flower` docker services.

#### CELERY_BROKER_URL

No default value (must be set).

Celery broker url. Used by flower worker.

#### REDIS_HOST

No default value (must be set).

Redis host.

#### REDIS_PORT

No default value (must be set).

Redis port.

## REST API

OpenAPI UI: `/api/v1/schema/`

Swagger scheme: `/api/v1/schema/swagger-ui/`
