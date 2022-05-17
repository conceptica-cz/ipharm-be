(environment-variables)=

# Environment variables

## iPharm variables

File: `./.envs/.development/.ipharm_app`

Django application variables. Used by `ipharm-app`, `ipharm-worker`, `ipharm-beat`  docker services.

### ALLOWED_HOSTS

No default value (must be set).

Django `ALLOWED_HOSTS` - list of hosts separated by comma (or just `*`).

### BASE_ICISELNIKY_URL

Default: `http://iciselniky-app:8000/api/v1`

Base iCiselniky API url.

### ICISELNIKY_TOKEN

Default: emtpy value.

iCiselniky API token.

### BASE_UNIS_URL

Default: emtpy value.

Base UNIS API (patient API) url.

### UNIS_TOKEN

Default: emtpy value.

Unis API (patient API) token.

### DEBUG

Default: `False`

### ENVIRONMENT

Default: `production`

App's environment.

### LOG_LEVEL

Default: `INFO`

Logging level.

### SECRET_KEY

No default value (must be set).

Django secret key.

## Postgres variables

File: `./.envs/.development/.ipharm_postgres`

Postgres variables. Used by `ipharm-postgres` and also by `ipharm-app`, `ipharm-worker`, `ipharm-beat` docker services.

### POSTGRES_DB

No default value (must be set).

Postgres database name.

### POSTGRES_PASSWORD

No default value (must be set).

Postgres database password.

### POSTGRES_HOST

No default value (must be set).

Postgres database host.

### POSTGRES_PORT

No default value (must be set).

Postgres database port.

### POSTGRES_USER

No default value (must be set).

Postrgres database user.

## Redis variables

Redis variables. Used by `ipharm-redis` and also by `ipharm-app`, `ipharm-worker`, `ipharm-beat`, `ipharm-flower` docker services.

### CELERY_BROKER_URL

No default value (must be set).

Celery broker url. Used by flower worker.

### REDIS_HOST

No default value (must be set).

Redis host.

### REDIS_PORT

No default value (must be set).

Redis port.
