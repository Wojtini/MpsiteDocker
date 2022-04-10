from django.contrib.auth.models import User, Group
from rest_framework import serializers
from wotwatcher.models import TankExpectations, TankRatingSubscription
from home.models import EnvironmentVariable
from discordapp.models import Playlist, Song, PlaylistOwnership


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['name']


class TankExpectationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TankExpectations
        fields = ['tank_id', 'tank_name', 'exp_Def', 'exp_Frag', 'exp_Spot', 'exp_Damage', 'exp_WinRate']


class TankRatingSubscriptionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TankRatingSubscription
        fields = ['wot_username', 'tank', 'wn8', 'lastUpdate', 'dmgPerGame', 'fragPerGame', 'winRate']


class EnvironmentVariableSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EnvironmentVariable
        fields = ['name', 'value']


class PlaylistSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Playlist
        fields = ['name', 'desc', 'active']


class PlaylistOwnershipSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PlaylistOwnership
        fields = ['playlist', 'user']


class SongSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Song
        fields = ['name', 'url', 'playlist']
