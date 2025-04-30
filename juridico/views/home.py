from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.contrib import messages
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

import pandas as pd
from io import BytesIO
import os
from ..forms import ProcessoForm, AdvogadoForm, ProcessoFilterForm
from ..models import Advogado, Processo


# ===== Renderizar a tela Home se o login for bem sucedido =====
@login_required
def home(request):
    processo_form = ProcessoForm()
    advogado_form = AdvogadoForm()
    processos = Processo.objects.all()  

    filter_form = ProcessoFilterForm(request.GET) # Inicializa o formulário de filtro com os dados GET

    if filter_form.is_valid():
        numero_processo = filter_form.cleaned_data.get('numero_processo')
        status = filter_form.cleaned_data.get('status')
        instancia = filter_form.cleaned_data.get('instancia')
        nome_autor = filter_form.cleaned_data.get('nome_autor')
        advogado = filter_form.cleaned_data.get('advogado')

        if numero_processo:
            processos = processos.filter(numero_processo__icontains=numero_processo)
        if status:
            processos = processos.filter(status=status)
        if instancia:
            processos = processos.filter(instancia=instancia)
        if nome_autor:
            processos = processos.filter(nome_autor=nome_autor)
        if advogado:
            processos = processos.filter(advogado=advogado)
        # Adicione mais filtros conforme os campos no seu formulário de filtro

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
    
    advogados = Advogado.objects.all()  # Busca todos os advogados

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'juridico/partials/processo_tabela.html', {
            'processos': processos
        })

    return render(request, 'juridico/home.html', {
        'processo_form': processo_form,
        'advogado_form': advogado_form,
        'advogados': advogados,
        'processos': processos,
        'filter_form': filter_form,
    })

def exportar_processos_pdf(request, numero_processo):
    try:
        processo = Processo.objects.get(numero_processo=numero_processo)
    except Processo.DoesNotExist:
        return HttpResponse("Processo não encontrado", status=404)

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    largura, altura = A4

    # Caminho da imagem do cabeçalho
    caminho_imagem = os.path.join(settings.BASE_DIR, "juridico", "static", "juridico", "img", "logo_fund_transp _02.png")

    # Adicionando a imagem no topo
    if os.path.exists(caminho_imagem):
        imagem = ImageReader(caminho_imagem)
        pdf.drawImage(imagem, 50, altura - 100, width=100, height=50, preserveAspectRatio=True)

    # Título do documento abaixo da imagem
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(200, altura - 80, f"Relatório do Processo {processo.numero_processo}")

    # Definição do ponto inicial para os dados
    y = altura - 150  # Primeira linha dos dados
    espacamento_vertical = 40  # Espaçamento entre as linhas
    espacamento_horizontal = 250  # Espaçamento entre as colunas

    # Organização dos dados para exibição
    dados = [
        ("Número do Processo", processo.numero_processo),
        ("Tipo", processo.tipo_processo),
        ("Autor", processo.nome_autor),
        ("Status", processo.status),
        ("Unidade", processo.unidade),
        ("Data de Propositura", processo.data_propositura.strftime('%d/%m/%Y')),
        ("Advogado", processo.advogado.nome_completo),
        ("Juiz", processo.juiz)
    ]

    # Ajustando para exibição em duas colunas
    for i in range(0, len(dados), 2):
        # Primeira coluna
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(50, y, dados[i][0])  # Nome do campo (negrito)
        pdf.setFont("Helvetica", 12)
        pdf.drawString(50, y - 15, str(dados[i][1]))  # Valor do campo

        # Segunda coluna (se existir)
        if i + 1 < len(dados):
            pdf.setFont("Helvetica-Bold", 12)
            pdf.drawString(50 + espacamento_horizontal, y, dados[i + 1][0])  # Nome do campo (negrito)
            pdf.setFont("Helvetica", 12)
            pdf.drawString(50 + espacamento_horizontal, y - 15, str(dados[i + 1][1]))  # Valor do campo

        # Descer para a próxima linha
        y -= espacamento_vertical

    # Adicionando o campo "Descrição" centralizado
    y -= 20  # Espaçamento extra antes da descrição
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawCentredString(largura / 2, y, "Descrição")  # Nome do campo centralizado
    y -= 15  # Espaço antes do valor

    pdf.setFont("Helvetica", 12)
    pdf.drawCentredString(largura / 2, y, processo.descricao)  # Valor da descrição centralizado

    # Finaliza o PDF
    pdf.save()
    buffer.seek(0)

    # Retorna o PDF como resposta
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Processo_{numero_processo}.pdf"'

    return response

def editar_processo(request):
    if request.method == "POST":
        try:
            processo_id = request.POST.get("id")
            processo = get_object_or_404(Processo, id=processo_id)

            # Campos básicos
            processo.unidade = request.POST.get("unidade", processo.unidade)
            processo.tipo_processo = request.POST.get("tipo_processo", processo.tipo_processo)
            processo.acao = request.POST.get("acao", processo.acao)
            processo.contrato_envolvido = request.POST.get("contrato_envolvido", processo.contrato_envolvido)
            processo.cidade = request.POST.get("cidade", processo.cidade)
            processo.valor_causa = float(request.POST.get("valor_causa", processo.valor_causa) or 0.0)
            processo.vara = request.POST.get("vara", processo.vara)
            processo.fase = request.POST.get("fase", processo.fase)
            processo.instancia = request.POST.get("instancia", processo.instancia)
            processo.data_propositura = request.POST.get("data_propositura", processo.data_propositura)
            processo.status = request.POST.get("status", processo.status)
            processo.nome_autor = request.POST.get("nome_autor", processo.nome_autor)
            processo.cpf_autor = request.POST.get("cpf_autor", processo.cpf_autor)
            processo.data_ultima_modificacao = request.POST.get("data_ultima_modificacao", processo.data_ultima_modificacao)
            processo.juiz = request.POST.get("juiz", processo.juiz)
            processo.numero_processo = request.POST.get("numero_processo", processo.numero_processo)
            processo.descricao = request.POST.get("descricao", processo.descricao)

            # Verifica se o advogado existe
            advogado_id = request.POST.get("advogado")
            if advogado_id:
                advogado = get_object_or_404(Advogado, id=advogado_id)
                processo.advogado = advogado

            processo.save()

            return JsonResponse({"success": True, "message": "Processo atualizado com sucesso."})

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Método inválido"})

def excluir_processo(request, id):
    processo = get_object_or_404(Processo, id=id)
    try:
        processo.delete()
        messages.success(request, "Processo excluído com sucesso.")
    except Exception as e:
        messages.error(request, f"Ocorreu um erro ao tentar excluir: {e}")
    return redirect('home')  # Redirecionando para a view unificada

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