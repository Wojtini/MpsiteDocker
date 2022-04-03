from django.urls import path

from . import views

app_name = "movierating"
urlpatterns = [
    path('', views.index, name='list'),
    path('addMovie', views.addmovierequest),
    path('addReview', views.addreviewrequest),
    path('addReview/<str:moviename>', views.addreviewrequest),
]

