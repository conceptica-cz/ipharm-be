from django.contrib.auth.middleware import RemoteUserMiddleware


class KerberosUserMiddleware(RemoteUserMiddleware):
    header = "HTTP_X_REMOTE_USER"
