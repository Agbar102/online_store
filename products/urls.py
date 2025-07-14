from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ItemCRUDAdminViewSet, ItemListViewSet, CategoryCRUDViewSet, SubCategoryCRUDViewSet, FavoriteViewSet

router = DefaultRouter()
router.register(r'admin/items', ItemCRUDAdminViewSet, basename='admin-items')
router.register(r'items', ItemListViewSet, basename='items')
router.register(r'categories', CategoryCRUDViewSet, basename='categories')
router.register(r'sub_categories', SubCategoryCRUDViewSet, basename='sub_categories')
router.register(r'favorites', FavoriteViewSet, basename='favorites')

urlpatterns = [
    path('', include(router.urls)),
]