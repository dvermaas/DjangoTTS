import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Enquete, Question, Choice, Vote
from django.urls import reverse

from members.views import *
from django.contrib.auth.models import User

# factory boy
def create_enquete(text="default", days=timezone.now()):
    time = timezone.now() + datetime.timedelta(days=days)
    return Enquete.objects.create(text=text, pub_date=time)

def create_question(enquete, text="default"):
    return Question.objects.create(enquete = enquete, text=text)

def create_choice(question, text="default"):
    return Choice.objects.create(question=question, text=text)

def create_vote(question, user, choice):
    #return Vote.obects.create(question = question, user=user, choice = choice)
    vote = Vote(question=question, user=user, choice=choice)
    vote.save()

class EnqueteIndexViewTests(TestCase):
    def setUp(self):
        # login
        self.user = User.objects.create_user(
            username= "testuser",
            password = "12345",
        )
        response = self.client.post("/members/login_user", {"username": self.user.username, "password": "12345"})
        self.assertRedirects(response, reverse("polls:index"))

    def test_no_enquetes(self):
        """
        If no enquetes exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No enquetes are available.")
        self.assertQuerysetEqual(response.context['latest_enquete_list'], [])

    def test_past_enquete(self):
        """
        Enquetes with a pub_date in the past are displayed on the
        index page.
        """
        enquete = create_enquete(days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_enquete_list'],
            [enquete],
        )

    def test_future_enquete(self):
        """
        Enquetes with a pub_date in the future aren't displayed on
        the index page.
        """
        enquete = create_enquete(days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No enquetes are available.")
        self.assertQuerysetEqual(response.context['latest_enquete_list'], [])

    def test_future_enquete_and_past_enquete(self):
        """
        Even if both past and future enquetes exist, only past enquetes
        are displayed.
        """
        enquete1 = create_enquete(days=-30)
        enquete2 = create_enquete(days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_enquete_list'],
            [enquete1],
        )

    def test_two_past_enquetes(self):
        """
        The enquetes index page may display multiple questions.
        """
        enquete1 = create_enquete(days=-30)
        enquete2 = create_enquete(days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_enquete_list'],
            [enquete2, enquete1],
        )

    def test_pending_enquete(self):
        """
        Check if not voted on enquete is in pending list
        """
        # create enquete
        enquete = create_enquete(days=-30)
        create_question(enquete)
        
        # see if it is in the pending list
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['enquete_pending_list'],
            [enquete],
        )

    def test_done_enquete(self):
        """
        Check if not voted on enquete is in done list if done
        """
        # create enquete
        enquete = create_enquete(days=-30)
        question = create_question(enquete)
        choice = create_choice(question)
        create_vote(question, self.user, choice)
        
        # see if it is done
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['enquete_done_list'],
            [enquete],
        )

class QuestionDetailViewTests(TestCase):
    def setUp(self):
        # login
        self.user = User.objects.create_user(
            username= "testuser",
            password = "12345",
        )
        response = self.client.post("/members/login_user", {"username": self.user.username, "password": "12345"})
        self.assertRedirects(response, reverse("polls:index"))

    def test_first_relevant_question_first(self):
        """
        Check if get_first_relevant_question() shows the first question
        """
        enquete = create_enquete(days=-30)
        question1 = create_question(enquete)
        create_choice(question1)
        question2 = create_question(enquete)
        create_choice(question2)
        self.assertEqual(enquete.get_first_relevant_question(self.user), question1)

    def test_first_relevant_question_second(self):
        """
        Check if get_first_relevant_question() shows the second question if first is answered
        """
        enquete = create_enquete(days=-30)
        question1 = create_question(enquete)
        choice1 = create_choice(question1)
        question2 = create_question(enquete)
        create_choice(question2)

        create_vote(question1, self.user, choice1)
        self.assertEqual(enquete.get_first_relevant_question(self.user), question2)
        
    def test_first_relevant_question_none(self):
        """
        Check if get_first_relevant_question() returns False if all questions are answered
        """
        enquete = create_enquete(days=-30)
        question1 = create_question(enquete)
        choice1 = create_choice(question1)
        question2 = create_question(enquete)
        choice2 = create_choice(question2)
        create_vote(question2, self.user, choice2)

        create_vote(question1, self.user, choice1)
        self.assertEqual(enquete.get_first_relevant_question(self.user), False)

class EnqueteModelTests(TestCase):

    def test_was_published_recently_with_future_enquete(self):
        """
        was_published_recently() returns False for enquetes whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_enquete = Enquete(pub_date=time)
        self.assertIs(future_enquete.was_published_recently(), False)

    def test_was_published_recently_with_old_enquete(self):
        """
        was_published_recently() returns False for enquetes whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_enquete = Enquete(pub_date=time)
        self.assertIs(old_enquete.was_published_recently(), False)

    def test_was_published_recently_with_recent_enquete(self):
        """
        was_published_recently() returns True for enquetes whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_enquete = Enquete(pub_date=time)
        self.assertIs(recent_enquete.was_published_recently(), True)