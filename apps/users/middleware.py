from django.contrib.auth.middleware import PersistentRemoteUserMiddleware


class KerberosUserMiddleware(PersistentRemoteUserMiddleware):
    header = "HTTP_X_REMOTE_USER"
