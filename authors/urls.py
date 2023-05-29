from django.urls import path 
from .views import RegisterAuthor, LoginAuthor

urlpatterns = [
    path("register/", RegisterAuthor.as_view()),
    path("login/", LoginAuthor.as_view()),
]
