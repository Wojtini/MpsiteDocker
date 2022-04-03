from django.urls import path

from . import views

app_name = 'home'
urlpatterns = [
    path('', views.index, name='index'),
    path('servers', views.servers_monitor, name='servers'),
    path('register', views.register_request, name='register'),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name="logout"),
    path("personnel", views.personnel, name="personnel"),
    path('profile/<str:username>', views.profile, name="profile"),
    path('editprofile', views.edit_profile, name="edit_profile"),
    path('edituser', views.edit_user, name="edit_user"),
]

