import random
from datetime import timedelta
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.utils import timezone
from django.utils.timezone import now
from users.models import CustomUser
from .tasks import send_message_register


User = get_user_model()


class RegisterUserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(min_length=8, write_only=True)
    password2 = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

    def validate_email(self, value):
        if not value.endswith('@gmail.com'):
            raise serializers.ValidationError("Регистрация разрешена только с @gmail.com")

        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Этот email уже зарегистрирован")
        return value


    def validate(self, attrs):
        password1 = attrs.pop("password1")
        password2 = attrs.pop("password2")
        if password1 != password2:
            raise serializers.ValidationError("Пароли не совпадают")
        attrs["password"] = password1
        return attrs


    def create(self, validate_data):
        email = validate_data["email"]
        password = validate_data["password"]

        user = User(email=email)
        user.set_password(password)
        user.is_active = False
        user.confirmation_code = str(random.randint(100000, 999999))
        user.confirmation_send = timezone.now()
        user.save()

        send_message_register.delay(user.email, user.confirmation_code)

        return user


class ActivateUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)

    def validate(self, attrs):
        email = attrs['email']
        code = attrs['code']

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Пользователь не найден")

        if user.is_active:
            raise serializers.ValidationError("Пользователь уже активирован")

        if now() - user.confirmation_send > timedelta(minutes=10):
            raise serializers.ValidationError("Код подтверждения истёк. Запросите новый.")

        if user.activation_attempts >= 5:
            block_time = user.last_activation_attempt + timedelta(minutes=5)
            if now() < block_time:
                raise serializers.ValidationError("Превышено количество попыток. Попробуйте через 5 минут.")
            else:
                user.activation_attempts = 0
                user.save()

        if user.confirmation_code != code:
            user.activation_attempts = user.activation_attempts + 1
            user.last_activation_attempt = now()
            user.save()
            raise serializers.ValidationError("Неверный код.")

        attrs['user'] = user
        return attrs

    def save(self, **kwargs):
        user = self.validated_data['user']
        user.is_active = True
        user.confirmation_code = None
        user.activation_attempts = 0
        user.save()
        return user


class UserEditProfileSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True, required=False)
    new_password = serializers.CharField(write_only=True, required=False, min_length=8)
    email = serializers.EmailField(required=False)

    class Meta:
        model = User
        fields = ['email', 'old_password', 'new_password']

    def validate(self, attrs):
        user = self.context['request'].user

        old_password = attrs.get('old_password')
        new_password = attrs.get('new_password')

        if new_password:
            if not old_password:
                raise serializers.ValidationError("Укажите свой старый пароль для смены пароля.")
            if not user.check_password(old_password):
                raise serializers.ValidationError("Старый пароль неверный")

        return attrs

    def update(self, instance, validated_data):
        email = validated_data.get('email')
        if email:
            instance.email = email

        new_password = validated_data.get('new_password')
        if new_password:
            instance.set_password(new_password)

        instance.save()
        return instance


