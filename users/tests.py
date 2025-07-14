import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from users.models import CustomUser


@pytest.mark.django_db
def test_register_user():
    client = APIClient()
    url = reverse('register/')
    data = {"email": "test@gmail.com", "password": "Qwert5566"}

    response = client.post(url, data)

    assert response.status_code == 201
    assert response.data["message"] == "Код отправлен на email"
    user = CustomUser.objects.get(gamil="test@gmail.com")
    assert user.is_active is False
    assert user.confirmation_code is not None


@pytest.mark.django_db
def test_activate_user():
    client = APIClient()
    user = CustomUser.objects.create_user(
        email="test@example.com",
        password="12345678",
        is_active=False,
        confirmation_code="123456"
    )
    response = client.post(reverse('activate/'),{
        "email": user.email,
        "code": "123456"

    })

    assert response.status_code == 200
    user.refresh_from_db()
    assert user.is_active
    assert user.confirmation_code is None
