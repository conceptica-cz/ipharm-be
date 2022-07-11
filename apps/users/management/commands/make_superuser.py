from django.core.management.base import BaseCommand
from rest_framework.authtoken.models import Token
from users.models import User

apps = ["requisitions"]


class Command(BaseCommand):
    help = "Make from a user a superuser"

    def add_arguments(self, parser):
        parser.add_argument(
            "username",
            help="Username of the user to make superuser",
        )

    def handle(self, *args, **options):
        username = options["username"]
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            print(f"User '{username}' does not exist.")
            return
        confirmation = input(
            f"It is a dangerous command!!! Are you sure you want to make user '{username}' a superuser? [y/N]:"
        )
        if confirmation.lower() == "y":
            user.is_staff = True
            user.is_superuser = True
            user.save()
            print(f"User '{username}' is now a superuser.")
        else:
            print("Operation canceled.")
