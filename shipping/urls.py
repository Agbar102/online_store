from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ShippingViewSet

router = DefaultRouter()
router.register(r'', ShippingViewSet, basename='shopping')

urlpatterns = [
    path('', include(router.urls)),
]