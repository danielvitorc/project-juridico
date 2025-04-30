from django.shortcuts import render, redirect
from django.http import JsonResponse
from ..forms import ReuniaoForm
from ..models import Processo, Reuniao


def reunioes(request):
    processos = Processo.objects.all()
    form_reuniao = ReuniaoForm()  # Inicializa o formulário vazio

    if request.method == "POST":
        form_reuniao = ReuniaoForm(request.POST)
        if form_reuniao.is_valid():
            form_reuniao.save()
            return redirect("reunioes")  # Redireciona para evitar reenvio do formulário

    return render(request, "juridico/reunioes.html", {"form_reuniao": form_reuniao, "processos": processos})

def api_reunioes(request):
    reunioes = Reuniao.objects.all()
    eventos = []
    
    for reuniao in reunioes:
        eventos.append({
            "title": f"Reunião - {reuniao.autor.nome_autor} ({reuniao.processo.numero_processo})",
            "start": f"{reuniao.data}T{reuniao.hora}",  
            "description": reuniao.descricao,
            "autor": str(reuniao.autor.nome_autor),  # Converte para string
            "processo": f"{reuniao.processo} "  
        })
    
    return JsonResponse(eventos, safe=False)

def get_processos_por_autor(request):
    autor_nome = request.GET.get("autor")
    
    if autor_nome:
        processos = Processo.objects.filter(nome_autor=autor_nome).values("id", "numero_processo", "tipo_processo")
        return JsonResponse(list(processos), safe=False)
    
    return JsonResponse([], safe=False)