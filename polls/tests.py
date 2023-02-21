import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Question, Sequence
from django.urls import reverse

def create_sequence(sequence_text="default", days=timezone.now()):
    time = timezone.now() + datetime.timedelta(days=days)
    return Sequence.objects.create(sequence_text=sequence_text, pub_date=time)

def create_question(sequence, question_text="default", days=timezone.now()):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    sequence = sequence
    return Question.objects.create(question_text=question_text, pub_date=time)

class SequenceIndexViewTests(TestCase):
    def test_no_sequences(self):
        """
        If no sequences exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No enquetes are available.")
        self.assertQuerysetEqual(response.context['latest_sequence_list'], [])

    def test_past_sequence(self):
        """
        Sequences with a pub_date in the past are displayed on the
        index page.
        """
        sequence = create_sequence(days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_sequence_list'],
            [sequence],
        )

    def test_future_sequence(self):
        """
        Sequences with a pub_date in the future aren't displayed on
        the index page.
        """
        sequence = create_sequence(days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No enquetes are available.")
        self.assertQuerysetEqual(response.context['latest_sequence_list'], [])

    def test_future_sequence_and_past_sequence(self):
        """
        Even if both past and future sequences exist, only past sequences
        are displayed.
        """
        sequence1 = create_sequence(days=-30)
        sequence2 = create_sequence(days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_sequence_list'],
            [sequence1],
        )

    def test_two_past_sequences(self):
        """
        The sequences index page may display multiple questions.
        """
        sequence1 = create_sequence(days=-30)
        sequence2 = create_sequence(days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_sequence_list'],
            [sequence2, sequence1],
        )

    def test_pending_sequence(self):
        sequence1 = create_sequence(days=-30)
        question1 = create_question(sequence1, days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['sequence_done_list'],
            [sequence1],
        )

class QuestionDetailViewTests(TestCase):
    pass
     
class SequenceModelTests(TestCase):

    def test_was_published_recently_with_future_sequence(self):
        """
        was_published_recently() returns False for sequences whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_sequence = Sequence(pub_date=time)
        self.assertIs(future_sequence.was_published_recently(), False)

    def test_was_published_recently_with_old_sequence(self):
        """
        was_published_recently() returns False for sequences whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_sequence = Sequence(pub_date=time)
        self.assertIs(old_sequence.was_published_recently(), False)

    def test_was_published_recently_with_recent_sequence(self):
        """
        was_published_recently() returns True for sequences whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_sequence = Sequence(pub_date=time)
        self.assertIs(recent_sequence.was_published_recently(), True)