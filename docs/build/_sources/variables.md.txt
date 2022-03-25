(environment-variables)=

# Environment variables

## iPharm variables

File: `./.envs/.development/.ipharm_app`

Django application variables. Used by `ipharm-app`, `ipharm-worker`, `ipharm-beat`  docker services.

### ALLOWED_HOSTS

No default value (must be set).

Django `ALLOWED_HOSTS` - list of hosts separated by comma (or just `*`).

### BASE_IPHARM_REFERENCES_URL

Default: `http://iciselniky-app:8000/api/v1`

Base references API (iciselniky app) url.

### BASE_REFERENCES_URL

No default value (must be set).

External API (patient) url.

### DEBUG

Default: `False`

### ENVIRONMENT

Default: `production`

App's environment.

### IPHARM_REFERENCES_TOKEN

No default value (must be set).

References API (iciselniky app) token.

### LOG_LEVEL

Default: `INFO`

Logging level.

### REFERENCES_TOKEN

No default value (must be set).

External API (patient) token.

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
