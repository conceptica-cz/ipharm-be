from django.core.management.base import BaseCommand
from rest_framework.authtoken.models import Token
from users.models import User

apps = ["requisitions"]


class Command(BaseCommand):
    help = "Create 3-rd party application's users and tokens, consuming the API (requisitions)"

    def handle(self, *args, **options):
        for app in apps:
            if not User.objects.filter(username=app).exists():
                password = User.objects.make_random_password()
                user = User.objects.create_user(
                    username=app,
                    password=password,
                )
                token = Token.objects.create(user=user)
                print(f"User {app} created with token {token}")
        print("Users was created.")
