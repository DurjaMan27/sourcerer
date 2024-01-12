from django.urls import path
from . import views

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("<str:username>", views.homepageAuthenticated, name="homepage-authenticated"),
    path("results/<int:searchID>", views.results, name="results"),
    path("<str:username>/results/<int:searchID>", views.resultsAuthenticated, name="results-authenticated"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("copyCitations/<int:searchID>", views.citations, name="citations"),
    path("<str:username>/previousSearches", views.previousSearches, name="previousSearches")
]
