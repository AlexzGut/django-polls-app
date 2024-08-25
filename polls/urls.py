from django.urls import path
from . import views

app_name = 'polls' #application namespace
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    # DetailView generic view expects the primary key value captured from the URL to be called "pk"
    path('<int:pk>', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]