from rest_framework import viewsets
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Review
from .serializers import ReviewSerializer

class ReviewCRUDViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @extend_schema(
        summary="Создать отзыв на товар",
        request=ReviewSerializer,
        responses={201: ReviewSerializer},
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)