from django.contrib.auth.models import User, Group
from rest_framework import serializers
from wotwatcher.models import TankExpectations, TankRatingSubscription


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
