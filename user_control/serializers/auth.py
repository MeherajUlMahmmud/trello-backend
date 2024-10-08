from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.serializers import (
    Serializer, ModelSerializer, CharField, EmailField, ValidationError,
)
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from user_control.models import UserModel


class RegisterSerializer(ModelSerializer):
    first_name = CharField(max_length=255, min_length=3, required=False)
    last_name = CharField(max_length=255, min_length=3, required=False)
    password1 = CharField(write_only=True)
    password2 = CharField(write_only=True)

    class Meta:
        model = UserModel
        fields = [
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        password1 = data.get("password1", "")
        password2 = data.pop("password2", "")

        if password1 != password2:
            raise ValidationError("Passwords must match.")

        return data

    def create(self, validated_data):
        user = UserModel.objects.create_user(**validated_data)
        return user


class EmailVerificationSerializer(ModelSerializer):
    token = CharField(max_length=555)

    class Meta:
        model = UserModel
        fields = ['token']


class ResendVerificationEmailSerializer(ModelSerializer):
    email = EmailField(max_length=255, min_length=3)

    class Meta:
        model = UserModel
        fields = ['email']


class LoginSerializer(Serializer):
    email = EmailField(max_length=255, min_length=3)
    password = CharField(write_only=True)

    def validate(self, data):
        email = data.get("email", "")
        password = data.get("password", "")

        if email and password:
            user = authenticate(email=email, password=password)

            if not user:
                raise AuthenticationFailed('Invalid credentials, try again')
            if not user.is_active:
                raise AuthenticationFailed('Account disabled, contact admin')
            # if not user.is_verified:
            #     raise AuthenticationFailed('Account is not verified')

            return {
                'user': user,
                'tokens': user.tokens()
            }
        else:
            msg = "Must provide email and password both."
            raise ValidationError(msg)


class PasswordChangeSerializer(Serializer):
    email = EmailField(max_length=255, min_length=3)
    current_password = CharField(min_length=6, max_length=68, write_only=True)
    password1 = CharField(min_length=6, max_length=68, write_only=True)
    password2 = CharField(min_length=6, max_length=68, write_only=True)

    class Meta:
        fields = [
            'email',
            'current_password',
            'password1',
            'password2',
        ]

    def validate(self, attrs):
        email = attrs.get("email", "")
        current_password = attrs.get("current_password", "")
        password1 = attrs.get('password1')
        password2 = attrs.get('password2')

        if email and current_password:
            user = authenticate(email=email, password=current_password)

            if not user:
                raise AuthenticationFailed('Invalid credentials, try again')

        if password1 != password2:
            raise ValidationError('Passwords do not match')
        return attrs


class ResetPasswordRequestSerializer(Serializer):
    email = EmailField(min_length=2)

    class Meta:
        fields = [
            'email',
        ]


class SetNewPasswordSerializer(Serializer):
    password1 = CharField(min_length=6, max_length=68, write_only=True)
    password2 = CharField(min_length=6, max_length=68, write_only=True)

    class Meta:
        fields = [
            'password1',
            'password2',
        ]

    def validate(self, attrs):
        password1 = attrs.get('password1')
        password2 = attrs.get('password2')

        if password1 != password2:
            raise ValidationError('Passwords do not match')
        return attrs


class LogoutSerializer(Serializer):
    refresh = CharField()

    default_error_message = {
        'bad_token': 'Token is expired or invalid'
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail('bad_token')
