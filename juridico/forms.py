from django import forms
from .models import Processo, Advogado, Reuniao

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
        widgets = {
             'data_propositura': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
             'data_ultima_modificacao': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
    def clean(self):
        cleaned_data = super().clean()

        # Transforma todos os campos de texto em maiúsculo, se não forem None
        for field, value in cleaned_data.items():
            if isinstance(value, str):
                cleaned_data[field] = value.upper()

        return cleaned_data

class ProcessoFilterForm(forms.Form):
    numero_processo = forms.CharField(required=False, label='Nº do Processo', widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    status = forms.ChoiceField(
        required=False,
        label='Status',
        choices=[('', 'Todos')] + [
            ('PROCESSO EM TRÂMITE', 'PROCESSO EM TRÂMITE'), 
            ('PROCESSO SUSPENSO', 'PROCESSO SUSPENSO'),
            ('PROCESSO EXTINTO', 'PROCESSO EXTINTO')
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    instancia = forms.ChoiceField(
        required=False,
        label='Instância',
        choices=[('', 'Todas')] + [
            ('1ª INSTÂNCIA', '1ª INSTÂNCIA'), ('2ª INSTÂNCIA', '2ª INSTÂNCIA')
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    nome_autor = forms.CharField(required=False, label='RECLAMANTE', widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    advogado = forms.ModelChoiceField(
        queryset=Advogado.objects.all(),
        required=False,
        empty_label="Todos",
        label='Advogado',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pass


class ReuniaoForm(forms.ModelForm):
    class Meta:
        model = Reuniao
        fields = ['autor', 'processo', 'data', 'hora', 'descricao']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hora': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super(ReuniaoForm, self).__init__(*args, **kwargs)
        
        self.fields['autor'].queryset = Processo.objects.all()
        self.fields['autor'].label_from_instance = lambda obj: obj.nome_autor  # Mostra apenas o nome do autor

        self.fields['processo'].queryset = Processo.objects.all()
        self.fields['processo'].label_from_instance = lambda obj: f"{obj.numero_processo} - {obj.tipo_processo}"

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})