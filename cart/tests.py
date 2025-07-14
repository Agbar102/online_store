import pytest
from rest_framework.test import APIClient
from users.models import CustomUser
from products.models import Items

@pytest.fixture
def user():
    return CustomUser.objects.create_user(email="user@test.com", password="12345678")

@pytest.fixture
def item():
    return Items.objects.create(title="Phone", price=5000)

@pytest.mark.django_db
def test_add_item_to_cart(user, item):
    client = APIClient()
    client.force_authenticate(user)

    response = client.post("cart/add_item/", {
        "product": item.id,
        "quantity": 2
    })

    assert response.status_code == 201
    assert response.data["quantity"] == 2
    assert response.data["product"]["title"] == "Phone"

@pytest.mark.django_db
def test_update_cart_item(user, item):
    client = APIClient()
    client.force_authenticate(user)

    client.post("cart/add_item/", {
        "product": item.id,
        "quantity": 2
    })

    response = client.post("cart/update_item/", {
        "product": item.id,
        "quantity": 5
    })

    assert response.status_code == 200
    assert response.data["quantity"] == 5

@pytest.mark.django_db
def test_remove_cart_item(user, item):
    client = APIClient()
    client.force_authenticate(user)

    res = client.post("cart/add_item/", {
        "product": item.id,
        "quantity": 1
    })
    cart_item_id = res.data["id"]

    response = client.delete(f"cart/remove_item/{cart_item_id}/")
    assert response.status_code == 204
