from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from users.serializers import UserSerializer, PharmacistSerializer
from users.models import Pharmacist
from users.permissions import IsUser, IsSuperUser

User = get_user_model()


class UserRegister(APIView):
    def post(self, request: Request, format: str = "json") -> Response:
        serializer = UserSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        response = serializer.data
        response["refresh"] = str(refresh)
        response["access"] = str(refresh.access_token)

        return Response(response, status=status.HTTP_201_CREATED)


class UsersView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSuperUser]


class PharmacistCreateView(generics.ListCreateAPIView):
    serializer_class = PharmacistSerializer
    queryset = Pharmacist.objects.all()
    permission_classes = [IsAuthenticated, IsUser]

class PharmacistView(generics.ListCreateAPIView):
    serializer_class = PharmacistSerializer
    queryset = Pharmacist.objects.all()
    permission_classes = [IsAuthenticated, IsUser]


class PharmacistDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pharmacist.objects.all()
    permission_classes = [IsAuthenticated, IsUser]
    serializer_class = PharmacistSerializer
    lookup_field = "pharmacist"

    def delete(self, request, *args, **kwargs):
        self.destroy(request, *args, **kwargs)
        return  Response(
            {"message":"Profile Deleted Successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )
