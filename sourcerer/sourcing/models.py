from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass
class Result(models.Model):
    sourceCompany = models.TextField()
    sourceURL = models.URLField()
    summary = models.TextField()
    citation = models.TextField()
class Search(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    searchID = models.AutoField(primary_key=True)
    topic = models.TextField(max_length=255)
    numSources = models.IntegerField()
    citationFormat = models.CharField(max_length=3)
    searchDate = models.DateField()
    results = models.ManyToManyField(Result)