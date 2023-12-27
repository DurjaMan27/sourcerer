from django.shortcuts import render
from django.http import HttpResponse
from django import forms

# Create your views here.

class NewSearchForm(forms.Form):
    CATEGORY_CHOICES = [
        ('MLA', 'MLA'),
        ('APA', 'APA'),
        ('Chicago', 'Chicago'),
    ]

    topicQuestion = forms.CharField(label="Topic", widget=forms.TextInput(attrs={'placeholder': 'Research Question'}), required=True)
    startingBid = forms.IntegerField(label="Number of Sources", required=False)
    citationFormat = forms.ChoiceField(label="Citation Format", choices=CATEGORY_CHOICES, required=True)

def homepage(request):
    if request.method == 'POST':
        print("hello")
    else:
        return render(request, "sourcing/homepage.html", {
            'form': NewSearchForm
        })