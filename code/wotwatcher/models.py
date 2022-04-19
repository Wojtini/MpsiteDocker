from django.contrib import admin
from django.db import models
from django.contrib.auth.models import User
from django.db.models import ForeignKey


class TankExpectations(models.Model):
    tank_name = models.CharField(unique=True, max_length=150, null=True)
    tank_id = models.IntegerField(primary_key=True)
    exp_Def = models.FloatField()
    exp_Frag = models.FloatField()
    exp_Spot = models.FloatField()
    exp_Damage = models.FloatField()
    exp_WinRate = models.FloatField()

    def __str__(self):
        return f'{self.tank_name}'


class TankRatingSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wot_username = models.CharField(max_length=150)
    tank = models.ForeignKey(TankExpectations, on_delete=models.CASCADE)
    wn8 = models.IntegerField(null=False, default=0)
    lastUpdate = models.DateField(null=True)
    dmgPerGame = models.IntegerField(null=False, default=0)
    fragPerGame = models.FloatField(null=False, default=0)
    winRate = models.FloatField(null=False, default=0)
    spotPerGame = models.FloatField(null=False, default=0)
    defPerGame = models.FloatField(null=False, default=0)

    def __str__(self):
        return f"{self.user} watching {self.wot_username} on {self.tank.tank_name}"


admin.site.register(TankExpectations)
admin.site.register(TankRatingSubscription)
