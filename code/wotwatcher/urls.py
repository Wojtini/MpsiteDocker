from django.urls import path

from . import views


app_name = 'wotapi'
urlpatterns = [
    path('', views.list_menu, name='list'),
    path('add', views.add_menu),
    path('update', views.update_request),
]

