from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

import datetime
from.models import Question

# Create your tests here.
class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        The method was_published_recently() returns False for questions whose attribute pub_date is in the future
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        The method was_published_recently() returns False for questions whose attribute pub_date is older that 1 day
        """
        time = timezone.now() - datetime.timedelta(days=2)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        The method was_published_recently() returns False for questions whose attribute pub_date is within the last day
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

def create_question_with_choice(question_text, days):
    """
    Create a question with the given arguments.
    days is an offset to now (- to express a question published in the past,
    + to express a question published in the future, and
    0 to express the current date time)
    """
    time = timezone.now() + datetime.timedelta(days=days)
    # creates a new Question with one choice in the test database and returns the object created
    question = Question.objects.create(question_text=question_text, pub_date=time)
    question.choice_set.create(choice_text='choice', votes=0)
    return question

def create_question_without_choice(question_text, days):
    """
    Create a question with the given arguments.
    days is an offset to now (- to express a question published in the past,
    + to express a question published in the future, and
    0 to express the current date time)
    """
    time = timezone.now() + datetime.timedelta(days=days)
    # creates a new Question in the test database and returns the object created
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls are available')
        self.assertQuerySetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        question = create_question_with_choice('past_question', -3)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context['latest_question_list'], [question])

    def test_future_question(self):
        create_question_with_choice('future_question', 3)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls are available')
        self.assertQuerySetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        past_question = create_question_with_choice('past_question', -3)
        future_question = create_question_with_choice('future_question', 3)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context['latest_question_list'], [past_question])

    def test_two_past_questions(self):
        past_question_1 = create_question_with_choice('past_question_1', -1)
        past_question_2 = create_question_with_choice('past_question_2', -3)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context['latest_question_list'], [past_question_1, past_question_2])

    def test_past_question_without_choices(self):
        create_question_without_choice('no_choices', -3)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls are available')
        self.assertQuerySetEqual(response.context['latest_question_list'], [])   

class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
       future_question = create_question_with_choice('future_question', 5)
       # polls/<int:pk> receives a primary key as a url paramenter
       response = self.client.get(reverse('polls:detail', args=(future_question.pk,))) 
       self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        past_question = create_question_with_choice('past_question', -3)
        # polls/<int:pk> receives a primary key as a url paramenter
        response = self.client.get(reverse('polls:detail', args=(past_question.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, past_question.question_text)

    def test_past_question_without_choices(self):
        past_question_without_choices = create_question_without_choice('no_choices', -3)
        response = self.client.get(reverse('polls:detail', args=(past_question_without_choices.pk,))) 
        self.assertEqual(response.status_code, 404)

class QuestionResultsViewTests(TestCase):
    def test_future_question(self):
       future_question = create_question_with_choice('future_question', 5)
       # polls/<int:pk> receives a primary key as a url paramenter
       response = self.client.get(reverse('polls:results', args=(future_question.pk,))) 
       self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        past_question = create_question_with_choice('past_question', -3)
        # polls/<int:pk> receives a primary key as a url paramenter
        response = self.client.get(reverse('polls:results', args=(past_question.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, past_question.question_text)

    def test_past_question_without_choices(self):
        past_question_without_choices = create_question_without_choice('no_choices', -3)
        response = self.client.get(reverse('polls:results', args=(past_question_without_choices.pk,))) 
        self.assertEqual(response.status_code, 404)