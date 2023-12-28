from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from .models import User, Search, Result
from datetime import date, datetime
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import google.generativeai as genai
from django.utils import timezone

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


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("homepage"))
        else:
            return render(request, "sourcing/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "sourcing/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("homepage"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "sourcing/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "sourcing/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("homepage"))
    else:
        return render(request, "sourcing/register.html")

def homepage(request):
    if request.method == 'POST':
        form = NewSearchForm(request.POST)
        if form.is_valid():

            question = form.cleaned_data["topicQuestion"]
            numSources = form.cleaned_data["numSources"]
            citation = form.cleaned_data["citationFormat"]

            search = Search.objects.create(user=request.user, topic=question, numSources=numSources, citationFormat=citation, searchDate=str(date.today()))

            query = "My research topic/question is '" + question + "'. Given this question, please give me " + str(numSources) + " sources that will help me conduct research on the topic. "
            query += "These sources must be from reputable newspapers, magazines, encyclopedias, etc. No sources from Wikipedia. "
            query += "Along with the URLs to these sources, please give me a 1-2 sentence summary of each source as well as a(n) " + citation + " citation in proper format."
            query += "These sources must be in numbered format, with the content title first, the link next, the summary after, and the citation last. "
            query += "Please separate each requested item for each source with a ~"

            genai.configure(api_key="")
            model = genai.GenerativeModel('gemini-pro')

            response = model.generate_content(query)
            print(response.text)
            response = response.text.split(" ")
            print(response[0])

            for i in range(1, numSources+1):
                response = response[response.index(f"{i}.")]

                title, response = response[response.index("**Title:**")+9:response.index("**URL:**")]
                url, response = response[response.index("**URL:**")+7:response.index("**Summary:**")]
                summary, response = response[response.index("**Summary:**")+11:response.index("**Citation:**")]
                citation, response = response[response.index("**Citation**")+12]

                result = Result.objects.create(sourceCompany=title, sourceURL=url, summary=summary, citation=citation)
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