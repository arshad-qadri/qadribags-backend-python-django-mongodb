from django.urls import path
from .views import RegisterView, LoginView, GetLoggedInUser

urlpatterns = [
    path("register", RegisterView.as_view()),
    path("login", LoginView.as_view()),
    path("user", GetLoggedInUser.as_view()),
]
