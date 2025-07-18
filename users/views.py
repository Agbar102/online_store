from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.response import Response
from rest_framework import permissions, generics
from .serializers import RegisterUserSerializer, UserEditProfileSerializer, ActivateUserSerializer


User = get_user_model()


class RegisterUserAPIView(generics.CreateAPIView):
    serializer_class = RegisterUserSerializer
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        summary="Регистрация пользователя",
        request=RegisterUserSerializer,
        responses={201: OpenApiResponse(description="Код подтверждения отправлен на email")}
    )
    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({"message": "Код отправлен на email"}, status=201)


class ActivateAPIView(generics.GenericAPIView):
    serializer_class = ActivateUserSerializer
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        summary="Активация аккаунта по коду",
        request=ActivateUserSerializer,
        responses={200: OpenApiResponse(description="Аккаунт успешно активирован")}
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Аккаунт успешно активирован"})


@extend_schema(
    summary="Редактировать профиль пользователя",
)
class UserEditProfileApiview(generics.UpdateAPIView):
    serializer_class = UserEditProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
