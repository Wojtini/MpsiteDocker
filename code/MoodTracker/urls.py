from django.urls import path

from . import views

app_name = 'moodtracker'
urlpatterns = [
    path('', views.index, name='main'),
]

