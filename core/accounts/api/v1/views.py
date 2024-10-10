from rest_framework import generics
from . import serializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from mail_templated import EmailMessage
from .utils import EmailThread
from django.shortcuts import get_object_or_404
import jwt
from django.conf import settings
from jwt import exceptions


"""Getting base user information from Django"""
User = get_user_model()


class RegistrationAPIView(generics.GenericAPIView):

    serializer_class = serializers.RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            email = serializer.validated_data["email"]
            data = {"email": email}
            user_obj = get_object_or_404(User, email=email)
            token = self.get_token_for_user(user_obj)
            message = EmailMessage(
                "email/confirm_email.tpl",
                {"token": token},
                "from_email@gmail.com",
                to=[email],
            )
            EmailThread(message).start()
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class CustomObtainAuthToken(ObtainAuthToken):
    """To customize ObtainAuthToken to display email and ID in the output"""

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": token.key,
                "user_id": user.pk,
                "email": user.email,
            }
        )


class CustomDiscradAuthToken(APIView):
    """To destroy the token generated during logout"""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomTokenObtainPairView(TokenObtainPairView):
    """To customize the TokenObtainPairView to display the email and ID in the JWT output"""

    serializer_class = serializers.CustomTokenObtainPairSerializer


class ActivationAPIView(APIView):

    def get(self, request, token, *args, **kwargs):
        try:
            token = jwt.decode(
                token, settings.SECRET_KEY, algorithms=["HS256"]
            )
            user_id = token.get("user_id")
        except exceptions.ExpiredSignatureError:
            return Response(
                {"detail": "token is expired"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except exceptions.InvalidSignatureError:
            return Response(
                {"detail": "token is invalid"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_obj = User.objects.get(pk=user_id)

        if user_obj.is_active:
            return Response(
                {"detail": "your account is activated"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user_obj.is_active = True
        user_obj.save()
        return Response(
            {"detail": "your account have been activated successfully"},
            status=status.HTTP_200_OK,
        )


class ActivationResendAPIView(generics.GenericAPIView):
    serializer_class = serializers.ActivationSerializers

    def post(self, request, *args, **kwargs):
        serializer = serializers.ActivationSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_obj = serializer.validated_data["user"]
        token = self.get_token_for_user(user_obj)
        message = EmailMessage(
            "email/confirm_email.tpl",
            {"token": token},
            "from_email@gmail.com",
            to=[user_obj.email],
        )
        EmailThread(message).start()
        return Response(
            {"details": "send test email"}, status=status.HTTP_200_OK
        )

    def get_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class ChangePasswordAPIView(generics.GenericAPIView):
    """To change the password"""

    model = User
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.ChangePasswordSerializers

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(
                serializer.data.get("old_password")
            ):
                return Response(
                    {"Old Password": ["Wrong Password."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response(
                {"details": "Password Changed successfully"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetRequestAPIView(generics.GenericAPIView):
    serializer_class = serializers.ResetPasswordSendSerializers

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_obj = serializer.validated_data["user"]
        token = self.get_token_for_user(user_obj)
        message = EmailMessage(
            "email/password_reset.tpl",
            {"token": token},
            "from_email@gmail.com",
            to=[user_obj.email],
        )
        EmailThread(message).start()
        return Response(
            {"details": "send test email"}, status=status.HTTP_200_OK
        )

    def get_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class PasswordResetConfirmAPIView(generics.GenericAPIView):
    serializer_class = serializers.resetPasswordConfirmSerializer

    def post(self, request, token, *args, **kwargs):
        try:
            token = jwt.decode(
                token, settings.SECRET_KEY, algorithms=["HS256"]
            )
        except jwt.ExpiredSignatureError:
            return Response(
                {"detail": "token is expired"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except jwt.InvalidSignatureError:
            return Response(
                {"detail": "token is invalid"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(data=request.data)
        user_id = token.get("user_id")
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(
                {"detail": "User does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if serializer.is_valid():
            user.set_password(serializer.validated_data.get("new_password"))
            user.save()
            return Response(
                {"details": "Password changed successfully"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
