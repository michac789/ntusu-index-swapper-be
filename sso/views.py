from rest_framework import generics
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from NTUSU_BE.utils import send_email
from sso.models import User
from sso.permissions import IsSelfOrReadOnly, IsSuperUser
from sso.serializers import (
    EmailTestSerializer,
    TokenSerializer,
    UserCreateSerializer,
    UserProfileSerializer,
)


class EmailTestView(CreateAPIView):
    serializer_class = EmailTestSerializer
    permission_classes = [IsSuperUser]

    def post(self, request):
        serializer = EmailTestSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(send_email(
                subject=serializer.validated_data['subject'],
                body=serializer.validated_data['body'],
                recipients=serializer.validated_data['recipients'],
            ))


class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = 'username'
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsSelfOrReadOnly]


class UserVerifyView(APIView):
    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data['token']
        user = get_object_or_404(User, custom_token=token)
        user.is_active = True
        user.save()
        return Response({'status': 'account activated', })
