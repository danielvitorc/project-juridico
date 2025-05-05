from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def analitico(request):
    return render(request,'juridico/analitico.html')