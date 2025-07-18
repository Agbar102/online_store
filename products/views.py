from rest_framework import viewsets
from drf_spectacular.utils import extend_schema, OpenApiParameter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import permissions
from .permissions import IsAdminOrReadOnly
from .models import Items, Favorite, Category, SubCategory
from .serializers import PublicItemSerializer, AdminItemSerializer, FavoriteSerializer, CategorySerializer, \
    SubCategorySerializer, FavoriteCreateSerializer
from .filters import ItemFilter
from .paginations import LargeResultsSetPagination, FavoritePagination


class CategoryCRUDViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('-order')
    serializer_class = CategorySerializer
    permission_classes = []


class SubCategoryCRUDViewSet(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all().order_by('-id')
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = SubCategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category']


class ItemCRUDAdminViewSet(viewsets.ModelViewSet):
    queryset = Items.objects.all()
    serializer_class = AdminItemSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action in ['GET', 'HEAD', 'OPTIONS']:
            return PublicItemSerializer
        return AdminItemSerializer


class ItemListViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Items.objects.all().order_by('-id')
    serializer_class = PublicItemSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_class = ItemFilter
    pagination_class = LargeResultsSetPagination
    search_fields = ['title', 'description']

    @extend_schema(
        summary="Список товаров",
        description="Получение списка всех товаров с возможностью фильтрации и поиска по названию и описанию.",
        parameters=[
            OpenApiParameter(name='search', description='Поиск по названию и описанию товара', required=False, type=str),
            OpenApiParameter(name='subcategory', description='Фильтр по подкатегории', required=False, type=int),

        ],
        responses={200: PublicItemSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class FavoriteViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = FavoritePagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['items__title']
    search_fields = ['items__title']

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return FavoriteCreateSerializer
        return FavoriteSerializer

    @extend_schema(
        summary="Добавить товар в избранное",
        description="Добавляет товар в избранное текущему авторизованному пользователю.",
        request=FavoriteCreateSerializer,
        responses={201: FavoriteSerializer},
        tags=["Favorites"]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Список избранных товаров",
        description="Получить список всех товаров, добавленных в избранное пользователем.",
        tags=["Favorites"]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

