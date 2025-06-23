from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import APIException

User = get_user_model()


class GmailAPIExeption(APIException):
    status_code = 400
    default_detail = {"message":"Регистрация только по gmail"}



class RegisterUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password1 = serializers.CharField(min_length=8, write_only=True)
    password2 = serializers.CharField(min_length=8, write_only=True)

    def validate(self, attrs):
        email: str = attrs.get("email")
        user = User.objects.filter(email=email)
        if not email.endswith("@gmail.com"):
            raise GmailAPIExeption()
        if user.exists():
            raise serializers.ValidationError("Этот емейл уже занят!!!")
        password1 = attrs.pop("password1")
        password2 = attrs.pop("password2")
        if password1 == password2:
            attrs["password"] = password1
        else:
            raise serializers.ValidationError("Пароли не совпадают!!!")
        return attrs

# class LoginSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     password = serializers.CharField(min_length=8, write_only=True)
