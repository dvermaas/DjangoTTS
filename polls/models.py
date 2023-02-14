import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    voters = models.ManyToManyField(User, through="Vote")

    def __str__(self):
        return self.question_text

    def can_user_vote(self, user):
        user_votes = user.vote_set.all()
        qs = user_votes.filter(question=self)
        return not(qs.exists())

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def votes_list(self):
        return [choice.votes for choice in self.choice_set.all()]

    def total_votes(self):
        return 0
        return sum(self.votes_list())
    
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)

    @property
    def get_vote_count(self):
        return self.vote_set.count()
        
    def __str__(self):
        return self.choice_text

class Vote(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    voted_at = models.DateTimeField(auto_now_add=True)