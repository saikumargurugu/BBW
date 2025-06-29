from django.apps import AppConfig
from django.db.models.signals import post_migrate
import os  # Import os to check environment variables


class ShopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shop'

    def ready(self):
        # Check if the environment is local or development
        environment = os.getenv("DJANGO_ENV", "local")
        if environment in ["local", "dev"]:
            # Import populate_mock_data inside the ready method to avoid premature app loading
            from shop.shop_mockup import populate_mock_data

            def run_mock_data(sender, **kwargs):
                print("Running mock data population...")
                # populate_mock_data()

            post_migrate.connect(run_mock_data, sender=self)
