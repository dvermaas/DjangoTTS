from django.test import TestCase
from django.contrib.auth import get_user
from django.contrib.auth.models import User
from django.test import Client
from members.views import *
from django.urls import reverse

# Create your tests here.
class QuestionIndexViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username= "testuser",
            password = "12345",
        )

    def test_login(self):
        self.assertFalse(get_user(self.client).is_authenticated)
        response = self.client.post("/members/login_user", {"username": self.user.username, "password": "12345"})
        self.assertRedirects(response, reverse("polls:index"))
        self.assertTrue(get_user(self.client).is_authenticated)
        
        
    def test_wrong_login(self):
        self.assertFalse(get_user(self.client).is_authenticated) 
        response = self.client.post("/members/login_user", {"username": self.user.username, "password": "wrongpassword"})
        self.assertRedirects(response, "/members/login_user")
        self.assertFalse(get_user(self.client).is_authenticated)