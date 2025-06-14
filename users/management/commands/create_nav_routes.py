from django.core.management.base import BaseCommand
from users.models import Router, Organisation

class Command(BaseCommand):
    help = "Create nav routes in Router model for both public and private (auth) users"

    def handle(self, *args, **kwargs):
        nav_links = [
            {"label": "Home", "href": "/"},
            {"label": "Club", "href": "/club"},
            {"label": "Services", "href": "/services"},
            {"label": "Academy", "href": "/academy"},
            {"label": "Court Hire", "href": "/court-hire"},
            {"label": "Socials", "href": "/socials"},
            {"label": "Contact", "href": "/contact"},
            {"label": "Shop", "href": "/shop"},
            {"label": "Sign In", "href": "/sign-up"},
        ]

        # Optionally, get or create a default organisation
        # org, _ = Organisation.objects.get_or_create(name="Default Org")

        for is_auth in [False, True]:
            for link in nav_links:
                Router.objects.get_or_create(
                    url=link["href"],
                    label=link["label"],
                    is_auth_route=is_auth,
                    # organisation=org,
                )
        self.stdout.write(self.style.SUCCESS("Nav routes created for both public and private users."))