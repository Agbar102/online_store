from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ItemCRUDAdminViewSet, ItemListViewSet

router = DefaultRouter()
router.register(r'admin/items', ItemCRUDAdminViewSet, basename='admin-items')
router.register(r'items', ItemListViewSet, basename='items')

urlpatterns = [
    path('', include(router.urls)),
]