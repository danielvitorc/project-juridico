from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib import messages
import pandas as pd
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from .forms import ProcessoForm, AdvogadoForm
from .models import Advogado, Processo

# ===== Tela de Login ===== 
def login_usuario(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirecionar para a página inicial pós-login
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    return render(request, 'juridico/login.html')


# ===== Renderizar a tela Home se o login for bem sucedido =====
@login_required
def home(request):
    processo_form = ProcessoForm()
    advogado_form = AdvogadoForm()
    advogados = Advogado.objects.all()  # Busca todos os advogados
    processos = Processo.objects.all()  # Busca todos os processos

    if request.method == 'POST':
        if 'processo_submit' in request.POST:  # Identifica o formulário de Processo
            processo_form = ProcessoForm(request.POST)
            if processo_form.is_valid():
                processo_form.save()
                return redirect('home')
        
        elif 'advogado_submit' in request.POST:  # Identifica o formulário de Advogado
            advogado_form = AdvogadoForm(request.POST)
            if advogado_form.is_valid():
                advogado_form.save()
                return redirect('home')
            
        elif 'upload_excel' in request.FILES:
            excel_file = request.FILES['upload_excel']
            try:
                df = pd.read_excel(excel_file)
                for _, row in df.iterrows():
                    Processo.objects.create(
                        unidade=row['unidade'],
                        tipo_processo=row['tipo_processo'],
                        acao=row['acao'],
                        contrato_envolvido=row['contrato_envolvido'],
                        cidade=row['cidade'],
                        valor_causa=row['valor_causa'],
                        vara=row['vara'],
                        fase=row['fase'],
                        instancia=row['instancia'],
                        data_propositura=row['data_propositura'],
                        advogado=row['advogado'],
                        status=row['status'],
                        nome_autor=row['nome_autor'],
                        cpf_autor=row['cpf_autor'],
                        data_ultima_modificacao=row['data_ultima_modificacao'],
                        juiz=row['juiz'],
                        numero_processo=row['numero_processo'],
                        descricao=row['descricao']
                    )
                return redirect('home')
            except Exception as e:
                print(f"Erro ao importar planilha: {e}")

    return render(request, 'juridico/home.html', {
        'processo_form': processo_form,
        'advogado_form': advogado_form,
        'advogados': advogados,
        'processos': processos
    })

def exportar_processos_excel(request):
    # Consulta todos os registros do modelo Processos
    processos = Processo.objects.all().values()
    
    # Converte os registros para um DataFrame
    df = pd.DataFrame(processos)
    
    # Cria a resposta em Excel
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Processos.xlsx"'
    
    # Salva o DataFrame no Excel
    with pd.ExcelWriter(response, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Processos')
    
    return response

def download_planilha_modelo(request):
    # Define as colunas exigidas
    colunas_modelo = [
        "unidade", "tipo_processo", "acao", "contrato_envolvido", "cidade", "valor_causa", "vara", 
        "fase", "instancia", "data_propositura", "advogado", "status", 
        "nome_autor", "cpf_autor", "data_ultima_modificacao", "juiz", "numero_processo", 
        "descricao"
    ]
    
    # Cria um DataFrame vazio com essas colunas
    df = pd.DataFrame(columns=colunas_modelo)
    
    # Configura a resposta HTTP para download
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="Modelo_Processos.xlsx"'
    
    # Salva o DataFrame no arquivo Excel
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    
    return response

@login_required
def deletar_advogado(request, id):
    advogado = get_object_or_404(Advogado, id=id)
    advogado.delete()
    return redirect('home')

@login_required
def registros(request):
    return render(request,'juridico/registros.html')


# ==== Função para deslogar do sistema =====
def logout_usuario(request):
    logout(request)
    return redirect('login')