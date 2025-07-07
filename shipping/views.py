from rest_framework import viewsets, permissions
from .models import Shipping
from .permissions import IsAdminOrReadOnly
from .serializers import ShippingSerializer


class ShippingViewSet(viewsets.ModelViewSet):
    queryset = Shipping.objects.all()
    serializer_class = ShippingSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Shipping.objects.all()
        return Shipping.objects.filter(user=user)

