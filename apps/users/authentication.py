from rest_framework.authentication import RemoteUserAuthentication


class KerberosRemoteUserAuthentication(RemoteUserAuthentication):
    header = "HTTP_X_REMOTE_USER"
