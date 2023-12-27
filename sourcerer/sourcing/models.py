from django.db import models

# Create your models here.
class User(models.Model):
    pass

class Search(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.TextField(max_length=255)
    numSources = models.IntegerField(max_value=6)
    citationFormat = models.CharField(max_length=3)
    searchDate = models.DateField()

    results = []
    for i in range(numSources):
        results.append(models.ForeignKey(User, on_delete=models.CASCADE))

class Result(models.Model):
    sourceCompany = models.TextField()
    sourceURL = models.URLField()
    summary = models.TextField()
    citation = models.TextField()