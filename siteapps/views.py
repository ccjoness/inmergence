from django.shortcuts import render

#We added this to handle the HttpResponse in this particular manner.
from django.http.response import HttpResponse

# Create your views here.

def display_markup(request):
    return render(request, 'siteapps/markup.html')

def display_readings(request):
    return render(request, 'siteapps/readings.html')