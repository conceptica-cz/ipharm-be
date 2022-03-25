(getting-started)=

# Getting started

## Requirements

You need `docker` and `docker-compose` to run the app.

## Installation and configuration

### Clone the repository

```
$ git clone https://github.com/conceptica-cz/ipharm-be.git
```

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
