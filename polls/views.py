from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from .models import Choice, Question, Vote, Enquete
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
        context['latest_enquete_list'] = Enquete.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
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
    model = Enquete
    template_name = 'polls/results.html'

def index(request):
    latest_enquete_list = Enquete.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')
    enquete_pending_list, enquete_done_list = [], []
    if request.user.is_authenticated:
        for enquete in latest_enquete_list:
            if enquete.is_done(request.user):
                enquete_done_list.append(enquete)
            else:
                enquete_pending_list.append(enquete)
    
    context = {"latest_enquete_list": latest_enquete_list, 
               "enquete_pending_list": enquete_pending_list,
               "enquete_done_list": enquete_done_list}
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    next_question = question.enquete.get_first_relevant_question(request.user)
    if next_question == False:
        return HttpResponseRedirect(reverse('polls:results', args=(question.enquete.id,)))
    return render(request, 'polls/detail.html', {'question': next_question})

def results(request, enquete_id):
    enquete = get_object_or_404(Question, pk=enquete_id)
    return render(request, 'polls/results.html', {'question': enquete})

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
        elif not question.can_user_vote(request.user):
            messages.success(request, ("Nice try, but you already voted!"))
        else:
            vote = Vote(question=question, user=request.user, choice=selected_choice, pub_date=timezone.now())
            vote.save()
        
        next_question = question.enquete.get_first_relevant_question(request.user)
        if next_question:
            return HttpResponseRedirect(reverse('polls:detail', args=(next_question.id,)))
        else:
            return HttpResponseRedirect(reverse('polls:results', args=(question.enquete.id,)))
