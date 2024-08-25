from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db.models import F
from django.views import generic

from .models import Question, Choice

# Create your views here.
class IndexView(generic.ListView):
    # By default Django will look for a template called -> <app name>/<model name>_list.html
    template_name = 'polls/index.html' 
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
            Return the last five published questions
        """
        return Question.objects.order_by("-pub_date")[:5]

class DetailView(generic.DetailView):
    # By default Django will look for a template called -> <app name>/<model name>_detail.html
    template_name = 'polls/detail.html'
    model = Question
    


class ResultsView(generic.DetailView):
    # By default Django will look for a template called -> <app name>/<model name>_detail.html
    template_name = 'polls/results.html'
    model = Question


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        choice_id = request.POST['choice']
        selected_choice = question.choice_set.get(pk=choice_id)
    except (KeyError, Choice.DoesNotExist):
        context = {
            'question': question,
            'error_message': 'Choice was not selected',
            }
        return render(request, 'polls:detail', context)
    else:
        # Django uses the F() object to generate an SQL expression that
        # describes the required operation at the database level.
        # In this case we are incrementing the votes value of the selected choice by 1.
        selected_choice.votes = F('votes') + 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))
