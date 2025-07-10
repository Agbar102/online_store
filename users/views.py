from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.response import Response
from rest_framework import status, permissions, generics
from .serializers import RegisterUserSerializer, UserEditProfileSerializer, ActivateUserSerializer
from .tasks import send_message_register
from .models import CustomUser
from rest_framework.views import APIView
from django.utils import timezone
import random

User = get_user_model()


class RegisterUserAPIView(generics.GenericAPIView):
    serializer_class = RegisterUserSerializer
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        request=RegisterUserSerializer,
        responses={201: RegisterUserSerializer}
    )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        user = CustomUser(email=email)
        user.set_password(password)
        user.is_active = False
        user.save()

        code = f"{random.randint(100000, 999999)}"
        user.confirmation_code = code
        user.confirmation_send = timezone.now()
        user.save()

        send_message_register.delay(user.email, code)

        return Response({"message": "Код отправлен на email"}, status=status.HTTP_201_CREATED)


class ActivateAPIView(generics.GenericAPIView):
    serializer_class = ActivateUserSerializer
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        request=ActivateUserSerializer,
        responses={200: OpenApiResponse(description="Аккаунт успешно активирован")}
    )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        code = serializer.validated_data['code']

        try:
            user = CustomUser.objects.get(email=email, confirmation_code=code)
        except CustomUser.DoesNotExist:
            return Response({"error": "Неверный код или email"}, status=status.HTTP_400_BAD_REQUEST)

        user.is_active = True
        user.confirmation_code = None
        user.save()

        return Response({"message": "Аккаунт успешно активирован"})


class UserEditProfileApiview(generics.UpdateAPIView):
    serializer_class = UserEditProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user