from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import OrderItemViewSet

router = DefaultRouter()
router.register(r'orders', OrderItemViewSet, basename='orders')

urlpatterns = [
    path('', include(router.urls))
]