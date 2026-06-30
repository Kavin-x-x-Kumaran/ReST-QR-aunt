import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "REST_QR_aunt.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

username = os.environ["DJANGO_SUPERUSER_USERNAME"]

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(
        username=username,
        email=os.environ["DJANGO_SUPERUSER_EMAIL"],
        password=os.environ["DJANGO_SUPERUSER_PASSWORD"],
    )
    print("Superuser created.")
else:
    print("Superuser already exists.")