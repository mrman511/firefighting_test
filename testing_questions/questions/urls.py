from unicodedata import name
from django.urls import path
from . import views

urlpatterns=[
  path('question/', views.question, name='question'),
  # path('seed/', views.seed, name='seed_questions'),
]