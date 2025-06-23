from rest_framework import viewsets, generics
from rest_framework.permissions import IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from .permissions import IsAdminWithCustomMessage
from .models import Items
from .serializers import ItemSerializer
from .filters import ItemFilter
from .paginations import LargeResultsSetPagination


class ItemCRUDAdminViewSet(viewsets.ModelViewSet):
    queryset = Items.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAdminWithCustomMessage]


class ItemListViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Items.objects.all()
    serializer_class = ItemSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_class = ItemFilter
    pagination_class = LargeResultsSetPagination
    search_fields = ['title', 'description']




