from drf_spectacular.utils import extend_schema, OpenApiResponse
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer, CartItemUpsertSerializer


class CartViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def get_user_cart(self, user):
        cart, _ = Cart.objects.get_or_create(user=user)
        return cart

    def list(self, request):
        cart = self.get_user_cart(request.user)
        serializer = self.get_serializer(cart)
        return Response(serializer.data)

    @extend_schema(
        request=CartItemUpsertSerializer,
        responses={201: CartItemSerializer, 200: CartItemSerializer, 204: None}
    )

    @action(detail=False, methods=['POST'])
    def upsert_item(self, request):
        serializer = CartItemUpsertSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        item = serializer.save()

        if item is None:
            return Response({"message": "Товар удален из корзины"}, status=204)

        created = getattr(serializer, 'created', False)
        return Response(CartItemSerializer(item).data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


    @extend_schema(
        parameters=[
            OpenApiParameter(name='pk', type=OpenApiTypes.INT, location=OpenApiParameter.PATH)
        ],
        responses={
            204: OpenApiResponse(description="Товар удален"),
            404: OpenApiResponse(description="Товар не найден")
        }
    )

    @action(detail=True, methods=['delete'])
    def remove_item(self, request, pk=None):
        cart = self.get_user_cart(request.user)
        try:
            item = CartItem.objects.get(cart=cart, id=pk)
            item.delete()
            return Response({"message": "Товар удален"}, status=204)
        except CartItem.DoesNotExist:
            return Response({"error": "Товар не найден"}, status=404)