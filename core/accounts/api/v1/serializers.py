from rest_framework import serializers
from django.core import exceptions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializer register"""

    password1 = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "password1"]

        extra_kwargs = {
            "email": {"required": True},
        }

    def validate(self, attrs):
        email = attrs.get("email")
        if not email:
            raise serializers.ValidationError({"detail": "email is required"})

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"detail": "email is already registered"})

        if attrs.get("password") != attrs.get("password1"):
            raise serializers.ValidationError({"detail": "Password dose not match"})
        try:
            validate_password(attrs.get("password"))

        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})

        return super().validate(attrs)

    """Create a new user"""

    def create(self, validated_data):
        validated_data.pop("password1", None)
        return User.objects.create_user(**validated_data, is_active=False)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Adding custom fields to the token"""

    def validate(self, attrs):
        data = super().validate(attrs)

        data["email"] = self.user.email
        data["user_id"] = self.user.id

        return data


class ActivationSerializers(serializers.Serializer):
    email_or_username = serializers.CharField(required=True)

    def validate(self, attrs):
        email_or_username = attrs.get("email_or_username")
        if User.objects.filter(email=email_or_username).exists():
            try:
                user_obj = User.objects.get(email=email_or_username)
            except User.DoesNotExist:
                raise serializers.ValidationError({"detail": "User dose not exist"})
            if user_obj.is_active:
                raise serializers.ValidationError(
                    {"detail": "User is already activated and verified"}
                )
            attrs["user"] = user_obj
            return super().validate(attrs)
        else:
            try:
                user_obj = User.objects.get(username=email_or_username)
            except User.DoesNotExist:
                raise serializers.ValidationError({"detail": "User dose not exist"})
            if user_obj.is_active:
                raise serializers.ValidationError(
                    {"detail": "User is already activated and verified"}
                )
            attrs["user"] = user_obj
            return super().validate(attrs)


class ChangePasswordSerializers(serializers.Serializer):
    """Change user password and maintain security issues"""

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password1 = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs.get("new_password") != attrs.get("new_password1"):
            raise serializers.ValidationError({"detail": "Password dose not match"})
        try:
            validate_password(attrs.get("new_password"))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})

        return super().validate(attrs)


class ResetPasswordSendSerializers(serializers.Serializer):
    email = serializers.CharField(required=True)

    def validate(self, attrs):
        email = attrs.get("email")
        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"detail": "User dose not exist"})

        attrs["user"] = user_obj
        return super().validate(attrs)


class resetPasswordConfirmSerializer(serializers.Serializer):

    new_password = serializers.CharField(required=True)
    new_password1 = serializers.CharField(required=True)

    def validate(self, attrs):
        new_password = attrs.get("new_password")
        new_password1 = attrs.get("new_password1")
        if new_password != new_password1:
            raise serializers.ValidationError({"detail": "Password dose not match"})
        try:
            validate_password(new_password)
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})

        return super().validate(attrs)
