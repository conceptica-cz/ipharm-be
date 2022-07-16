from django.core.management.base import BaseCommand
from users.models import User


class Command(BaseCommand):
    help = "Add user to the 'ipharm' group"

    def add_arguments(self, parser):
        parser.add_argument(
            "username",
            help="Username of the user to add user to the 'ipharm' group",
        )

    def handle(self, *args, **options):
        username = options["username"]
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            print(f"User '{username}' does not exist.")
            return
        confirmation = input(
            f"It is a dangerous command!!! Are you sure you want to add user '{username}' to 'ipharm' group? [y/N]:"
        )
        if confirmation.lower() == "y":
            user.add_to_ipharm_group()
            print(f"User '{username}' has been added to the 'ipharm' group.")
        else:
            print("Operation canceled.")
