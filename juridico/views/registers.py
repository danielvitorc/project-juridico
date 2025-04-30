from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def registros(request):
    return render(request,'juridico/registros.html')