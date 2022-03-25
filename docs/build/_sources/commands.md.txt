# Django commands

Use `docker-compose` to run Django commands.
For example, to run the `create_sources` command:

```
$ docker-compose exec ipharm-app python manage.py create_sources
```

## create_sources

Create the sources for update ({meth}`updates.models.Source` instances). Sources are created from the `settings.UPDATE_SOURCES` list.

## create_reports

Create the generic report types ({meth}`reports.models.GenericReportType` instances). Report types are created from the `settings.GENERIC_REPORTS` list.

## create_beat

Create celery_beat periodic tasks ({meth}`reports.models.GenericReportType` instances).

## populate

Populate the database with fake data. This is useful for testing.

```{note}
Works only if the `settings.ENVIRONMENT` is `'development'`, `'local'` or `'test'`.
```
