from django.urls import path
from . import views

urlpatterns = [
    path("polls/hello", views.hello_world),
]