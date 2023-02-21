from django.test import TestCase
from django.contrib.auth import get_user
from django.contrib.auth.models import User
from django.test import Client

# Create your tests here.
class QuestionIndexViewTests(TestCase):
    def test_login(self):
        username='testuser', 
        password='12345'
        
        self.assertFalse(get_user(self.client).is_authenticated)
        user = User.objects.create(username=username)
        user.set_password(password)
        user.save()
        self.client.login(username=username, password=password)
        self.assertTrue(get_user(self.client).is_authenticated)

    def test_wrong_login(self):
        username='testuser', 
        password='12345'
        
        self.assertFalse(get_user(self.client).is_authenticated)
        user = User.objects.create(username=username)
        user.set_password(password)
        user.save()
        self.client.login(username=password, password=username)
        self.assertFalse(get_user(self.client).is_authenticated)