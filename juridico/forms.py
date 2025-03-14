from django import forms
from .models import Processo, Advogado

class AdvogadoForm(forms.ModelForm):
    class Meta:
        model = Advogado
        fields = ['oab', 'nome_completo']

class ProcessoForm(forms.ModelForm):
    UNIDADES_CHOICES = [
        ('AMAZONAS', 'AMAZONAS'),
        ('RORAIMA', 'RORAIMA'),
        ('MINAS GERAIS', 'MINAS GERAIS'),
    ]

    TIPO_PROCESSO_CHOICES = [
        ('CÍVEL', 'CÍVEL'),
        ('CRIMINAL', 'CRIMINAL'),
        ('PREVIDENCIARIO', 'PREVIDENCIARIO'),
        ('TRABALHISTA', 'TRABALHISTA'),
        ('VARA DE FAMILIA', 'VARA DE FAMILIA'),
    ]

    VARA_CHOICES = [
        ('CÍVEL', 'CÍVEL'),
        ('CONCILIAÇÃO', 'CONCILIAÇÃO'),
        ('INSTRUÇÃO E JULGAMENTO', 'INSTRUÇÃO E JULGAMENTO'),
        ('TRABALHISTA TRIBUTÁRIA', 'TRABALHISTA TRIBUTÁRIA'),
        ('VARA DE FAMILIA', 'VARA DE FAMILIA')
    ]

    FASE_CHOICES = [
        ('CONSTESTAÇÃO', 'CONSTESTAÇÃO'),
        ('CONCILIAÇÃO', 'CONCILIAÇÃO'),
        ('INPUGNAÇÃO', 'INPUGNAÇÃO'),
        ('INSTRUÇÃO', 'INSTRUÇÃO'),
        ('RECURSO', 'RECURSO'),
        ('SUSPENSO', 'SUSPENSO'),
        ('EXECUÇÃO', 'EXECUÇÃO'),
        ('EXECUÇÃO', 'EXECUÇÃO'),
        ('ARQUIVADO', 'ARQUIVADO'),
        ('ADMINISTRATIVO', 'ADMINISTRATIVO'),
        ('SOLICITAÇÃO DE DOCUMENTOS', 'SOLICITAÇÃO DE DOCUMENTOS'),
        
    ]

    INSTANCIA_CHOICES = [
        ('1ª INSTÂNCIA', '1ª INSTÂNCIA'),
        ('2ª INSTÂNCIA', '2ª INSTÂNCIA'),
    ]

    JUIZ_CHOICES = [
        ('SUBSTITUTO', 'SUBSTITUTO'),
        ('TITULAR', 'TITULAR'),
    ]
    
    STATUS_CHOICES = [
        ('PROCESSO EM TRÂMITE','PROCESSO EM TRÂMITE'),
        ('PROCESSO SUSPENSO','PROCESSO SUSPENSO'),
        ('PROCESSO EXTINTO','PROCESSO EXTINTO'),
    ]

    advogado = forms.ModelChoiceField(queryset=Advogado.objects.all(), empty_label="Selecione um advogado")
    unidade = forms.ChoiceField(choices=[('', 'Selecione uma unidade')] + UNIDADES_CHOICES)
    tipo_processo = forms.ChoiceField(choices=[('', 'Selecione')] + TIPO_PROCESSO_CHOICES)
    vara = forms.ChoiceField(choices=[('', 'Selecione')] + VARA_CHOICES)
    fase = forms.ChoiceField(choices=[('', 'Selecione')] + FASE_CHOICES)
    instancia = forms.ChoiceField(choices=[('', 'Selecione')] + INSTANCIA_CHOICES)
    juiz = forms.ChoiceField(choices=[('', 'Selecione')] + JUIZ_CHOICES)
    status = forms.ChoiceField(choices=[('','Selecione' )] + STATUS_CHOICES) 
    descricao = forms.Textarea()

    class Meta:
        model = Processo
        fields = [
            'unidade', 'tipo_processo', 'acao', 'contrato_envolvido', 'cidade', 'valor_causa', 'vara', 'fase', 'instancia',
            'data_propositura', 'advogado', 'status', 'nome_autor', 'cpf_autor', 'data_ultima_modificacao', 'juiz', 
            'numero_processo', 'descricao'
        ]
