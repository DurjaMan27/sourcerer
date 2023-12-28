from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from .models import User, Search, Result
from datetime import date
import google.generativeai as genai

# Create your views here.

class NewSearchForm(forms.Form):
    CATEGORY_CHOICES = [
        ('MLA', 'MLA'),
        ('APA', 'APA'),
        ('Chicago', 'Chicago'),
    ]
    topicQuestion = forms.CharField(label="Topic", widget=forms.TextInput(attrs={'placeholder': 'Research Question'}), required=True)
    numSources = forms.IntegerField(label="Number of Sources", required=False)
    citationFormat = forms.ChoiceField(label="Citation Format", choices=CATEGORY_CHOICES, required=True)

def homepage(request):
    if request.method == 'POST':
        form = NewSearchForm(request.POST)
        if form.is_valid():

            question = form.topicQuestion
            numSources = form.numSources
            citation = form.citationFormat

            search = Search.objects.create(user=request.user, topic=question, numSources=numSources, citation=citation, searchDate=date.today(), results=None)

            query = "My research topic/question is '" + question + "'. Given this question, please give me " + numSources + " sources that will help me conduct research on the topic. "
            query += "These sources must be from reputable newspapers, magazines, encyclopedias, etc. No sources from Wikipedia. "
            query += "Along with the URLs to these sources, please give me a 1-2 sentence summary of each source as well as a(n) " + citation + " citation in proper format."
            query += "These sources must be in numbered format, with the content title first, the link next, the summary after, and the citation last. "
            query += "Please separate each requested item for each source with a ~"

            genai.configure(api_key="")
            model = genai.GenerativeModel('gemini-pro')

            response = list(model.generate_content(query))

            for i in range(1, numSources+1):
                response = response[response.index(f"{i}.")]

                title, response = response[0:response.index("~")]
                url, response = response[1:response.index("~")]
                summary, response = response[1:response.index("~")]
                citation, response = response[1:response.index("~")]

                result = Result.objects.create(title=title, sourceURL=url, summary=summary, citation=citation)
                search.results.add(result)

            return HttpResponseRedirect(reverse('results', kwargs={'searchID': search.searchID}))
        else:
            return render(request, "sourcing/homepage.html", {
                'form': NewSearchForm
            })
    else:
        return render(request, "sourcing/homepage.html", {
            'form': NewSearchForm
        })

def results(request, searchID):
    search = Search.objects.get(pk=searchID)
    results = search.results.all()
    return render(request, "sourcing/results.html", {
        "search": search,
        "results": results
    })