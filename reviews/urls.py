from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReviewCRUDViewSet

router = DefaultRouter()
router.register('', ReviewCRUDViewSet, basename='rev')

urlpatterns = [
    path('', include(router.urls)),
]