from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from .models import Choice, Question, Vote, Sequence
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django. contrib import messages

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['latest_sequence_list'] = Sequence.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
        return context

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    latest_sequence_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list, 'latest_sequence_list': latest_sequence_list}
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        if not request.user.is_authenticated:
            messages.success(request, ("You can only vote after logging in!"))
            return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
        if not question.can_user_vote(request.user):
            messages.success(request, ("Nice try, but you already voted!"))
            return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

        vote = Vote(question=question, user=request.user, choice=selected_choice, pub_date=timezone.now())
        vote.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))