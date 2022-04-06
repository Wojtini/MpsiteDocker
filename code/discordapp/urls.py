from django.urls import path

from . import views

app_name = "discordapp"
urlpatterns = [
    path('', views.index, name='index'),
]

