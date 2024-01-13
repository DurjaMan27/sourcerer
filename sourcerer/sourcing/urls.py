from django.urls import path
from . import views

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("results/<int:searchID>", views.results, name="results"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("copyCitations/<int:searchID>", views.citations, name="citations"),
    path("<str:username>/savedSearches", views.savedSearches, name="savedSearches"),
    path("saveSearch/<int:searchID>", views.saveSearch, name="saveSearch")
]
