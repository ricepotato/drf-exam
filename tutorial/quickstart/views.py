from django.contrib.auth.models import Group, User
from rest_framework import authentication, permissions, viewsets
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView
from rest_framework import generics

from .serializers import GroupSerializer, UserSerializer, PlanSerializer
from .models import Plan


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class ListUsers(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        usersnames = [user.username for user in User.objects.all()]
        return Response(usersnames)


class OncePerSecondThrottle(UserRateThrottle):
    rate = "1/second"


@api_view(["GET", "POST"])
@throttle_classes([OncePerSecondThrottle])
def hello_world(request):
    return Response({"message": "Hello, world!"})


class PlanList(generics.ListCreateAPIView):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = PlanSerializer(queryset, many=True)
        return Response(serializer.data)
