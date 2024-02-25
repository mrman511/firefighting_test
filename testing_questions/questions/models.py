from django.db import models

# Create your models here.
class Question(models.Model):
  question=models.CharField(max_length=300, blank=True, null=True)
  a=models.CharField(max_length=300, blank=True, null=True)
  b=models.CharField(max_length=300, blank=True, null=True)
  c=models.CharField(max_length=300, blank=True, null=True)
  d=models.CharField(max_length=300, blank=True, null=True)
  answer=models.CharField(max_length=300, blank=True, null=True)