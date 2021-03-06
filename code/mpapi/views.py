from django.contrib.auth.models import User, Group
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework import permissions
from mpapi.serializers import UserSerializer, GroupSerializer
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from wotwatcher.models import TankExpectations, TankRatingSubscription
from mpapi.serializers import TankExpectationSerializer, TankRatingSubscriptionSerializer
from rest_framework.response import Response
from wotwatcher.views import update_wn8
from home.models import EnvironmentVariable
from mpapi.serializers import EnvironmentVariableSerializer
from discordapp.models import Playlist, PlaylistOwnership, Song
from mpapi.serializers import PlaylistSerializer, PlaylistOwnershipSerializer, SongSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 4
    page_size_query_param = 'page_size'
    max_page_size = 1000


class UserViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    # permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    # permission_classes = [permissions.IsAuthenticated]


class TankExpectationViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']
    queryset = TankExpectations.objects.all()
    serializer_class = TankExpectationSerializer
    # permission_classes = [permissions.IsAuthenticated]


class PlaylistViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer


class PlaylistOwnershipViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']
    queryset = PlaylistOwnership.objects.all()
    serializer_class = PlaylistOwnershipSerializer


class SongViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']
    queryset = Song.objects.all()
    serializer_class = SongSerializer


class EnvironmentVariableViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']
    queryset = EnvironmentVariable.objects.all()
    serializer_class = EnvironmentVariableSerializer

    def get_queryset(self):
        name = self.request.query_params.get('name')
        if name is None:
            return self.queryset
        result = self.queryset.filter(name=name)
        return result


class TankRatingSubscriptionViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post']
    queryset = TankRatingSubscription.objects.all()
    serializer_class = TankRatingSubscriptionSerializer
    # permission_classes = [permissions.IsAuthenticated]

    @action(detail=False)
    def update_wn8_stats(self, request):
        update_wn8()
        return Response(status=200)
