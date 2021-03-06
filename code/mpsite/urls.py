"""mpsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include
from rest_framework import routers
from mpapi import views
from django.views.static import serve


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'tankexpectations', views.TankExpectationViewSet)
router.register(r'tankratings', views.TankRatingSubscriptionViewSet)
router.register(r'environmentvariables', views.EnvironmentVariableViewSet)
router.register(r'playlist_ownership', views.PlaylistOwnershipViewSet)
router.register(r'playlist', views.PlaylistViewSet)
router.register(r'song', views.SongViewSet)


urlpatterns = [
    path('', include('home.urls')),
    path('admin/', admin.site.urls),
    path('movierating/', include('movierating.urls')),
    path('wotapi/', include('wotwatcher.urls')),
    path('discord/', include('discordapp.urls')),
    path('wine/', include('wineapp.urls')),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
