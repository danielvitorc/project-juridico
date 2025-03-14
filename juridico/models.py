from django.db import models


class Advogado(models.Model):
    oab = models.CharField(max_length=100)
    nome_completo = models.CharField(max_length=255)

    def __str__(self):
        return self.nome_completo

class Processo(models.Model):
    unidade = models.CharField(max_length=50)
    tipo_processo = models.CharField(max_length=50)
    acao = models.CharField(max_length=100)
    contrato_envolvido = models.CharField(max_length=100)
    cidade = models.CharField(max_length=50)
    valor_causa = models.FloatField()
    vara = models.CharField(max_length=50)
    fase = models.CharField(max_length=50)
    instancia = models.CharField(max_length=50)
    data_propositura = models.DateField()
    advogado = models.ForeignKey(Advogado, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    nome_autor = models.CharField(max_length=50, unique=True)
    cpf_autor = models.CharField(max_length=14)
    data_ultima_modificacao = models.DateField()
    juiz = models.CharField(max_length=50)
    numero_processo = models.CharField(max_length=50, unique=True)
    descricao = models.TextField()

    def __str__(self):
        return f"{self.numero_processo} - {self.tipo_processo}"

class Reuniao(models.Model):
    autor = models.ForeignKey(Processo, on_delete=models.CASCADE, related_name='reunioes_autor', to_field='nome_autor')
    processo = models.ForeignKey(Processo, on_delete=models.CASCADE, related_name='reunioes_processo', to_field='numero_processo')
    data = models.DateField()
    hora = models.TimeField()
    descricao = models.TextField()

    def __str__(self):
        return f'Reunião de {self.autor} para o Processo {self.processo} em {self.data} às {self.hora}'
