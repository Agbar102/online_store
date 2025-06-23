from rest_framework import viewsets, generics
from rest_framework.permissions import IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import permissions

from .permissions import IsAdminWithCustomMessage
from .models import Items, Favorite
from .serializers import PublicItemSerializer, AdminItemSerializer, FavoriteSerializer
from .filters import ItemFilter
from .paginations import LargeResultsSetPagination


class ItemCRUDAdminViewSet(viewsets.ModelViewSet):
    queryset = Items.objects.all()
    serializer_class = AdminItemSerializer
    permission_classes = [IsAdminWithCustomMessage]


class ItemListViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Items.objects.all()
    serializer_class = PublicItemSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_class = ItemFilter
    pagination_class = LargeResultsSetPagination
    search_fields = ['title', 'description']


class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


