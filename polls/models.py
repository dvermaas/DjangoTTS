import datetime
from django.utils import timezone
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string


class Enquete(models.Model):
    text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published", default=timezone.now,
                                    help_text="wanneer enquete word weergegeven")

    def __str__(self):
        return self.text

    def is_done(self, user):
        return self.get_first_relevant_question(user) is None

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def get_first_relevant_question(self, user):
        for question in self.question_set.all():
            if question.can_user_vote(user):
                return question
        return None

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


@receiver(post_save, sender=Enquete)
def send_mail_to_subs(sender, instance, created, **kwargs):
    if not created:
        return

    for user in User.objects.all():
        html_message = render_to_string('polls/email.html',
                                        {'recipient_name': user.username, 'poll_name': instance.text})
        email = EmailMessage(
            subject="New Poll Available!",
            body=html_message,
            from_email='myemail@example.com',
            to=[user.email],
        )
        email.content_subtype = 'html'
        email.send()


class Question(models.Model):
    text = models.CharField(max_length=200)
    voters = models.ManyToManyField(User, through="Vote")
    enquete = models.ForeignKey(Enquete, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

    def can_user_vote(self, user):
        user_votes = user.vote_set.all()
        qs = user_votes.filter(question=self)
        return not (qs.exists())

    def votes_list(self):
        return [choice.get_vote_count for choice in self.choice_set.all()]

    def total_votes(self):
        return sum(self.votes_list())


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)

    @property
    def get_vote_count(self):
        return self.vote_set.count()

    def __str__(self):
        return f"{self.question} | {self.text}"


class Vote(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    pub_date = models.DateTimeField("date published", default=timezone.now)

    def __str__(self):
        return f"<{self.user}> voted <{self.choice.text}> on <{self.question.text}>"
