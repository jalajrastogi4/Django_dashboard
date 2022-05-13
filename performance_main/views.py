from django.shortcuts import render
import altair as alt

def home(request):
    context = {
        'alt': alt
    }
    return render(request, 'index.html', context=context)