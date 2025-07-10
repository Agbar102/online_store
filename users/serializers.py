from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import APIException

User = get_user_model()


class GmailAPIExeption(APIException):
    status_code = 400
    default_detail = {"message":"Регистрация только по gmail"}



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
        user = User.objects.create_user(email=validate_data["email"],
                                        password=validate_data["password"]
                                        )
        user.is_active = False
        user.save()
        return user


class ActivateUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)


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


