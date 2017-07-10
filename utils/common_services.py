import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from main.variables import username, password


@pytest.mark.django_db
class CommonTestMethods:
    @classmethod
    def get_client_with_csrf_token(cls):
        client = APIClient(enforce_csrf_checks=False)       # We can do it with token,
        client.login(username=username, password=password)  # but for this need MORE time and HTML-page + CSRF
        return client

    @classmethod
    def create_superuser(cls):
        return User.objects.create_superuser(email="xxx@xxx.xxx", password='pass', username="user")
