from django.urls import path, include
from rest_framework.routers import DefaultRouter
from cart.views import CartViewSet
from orders.views import CheckoutView

router = DefaultRouter()
router.register(r'', CartViewSet, basename='cart')

urlpatterns = [
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('', include(router.urls))
]