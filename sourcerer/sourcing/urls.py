from django.urls import path
from . import views

urls = [
    path("", views.homepage, name="homepage")
]
