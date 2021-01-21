from django.urls import path

from . import views

urlpatterns = [
    path("", views.index),
    path("profiles/<username>/", views.profile),
    path("profiles/", views.profiles),
]
