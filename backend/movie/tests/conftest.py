import pytest
from django.contrib.auth.models import User


@pytest.fixture
def seller():
    data = {
        "username": "jordan",
        "first_name": "Jordan",
        "last_name": "Belfort",
        "email": "belfort@email.com"
    }
    user = User.objects.create(**data)
    return user
