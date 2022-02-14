from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from .models import batting_innings
from .models import record_run_streak
# Create your views here.
class InningsList(ListView):
    model=batting_innings

def run_streak(request):
    top_5=record_run_streak(100)
    return render(request, 'mystats/record.html',
                  {"top_5":top_5} )