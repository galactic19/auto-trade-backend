from django.http import HttpResponse
from django.shortcuts import render

def dashboard(request, *args, **kwargs):
    return HttpResponse("Dashboard")