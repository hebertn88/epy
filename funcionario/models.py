from django.db import models
from setor.models import Setor

# Create your models here.

class Funcionario(models.Model):
    nome = models.CharField(max_length=25)
    sobrenome = models.CharField(max_length=75)
    ativo = models.BooleanField(default=True)
    setor = models.ForeignKey(Setor, on_delete=models.PROTECT)

    def __str__(self):
        return self.nome

    @property
    def nome_completo(self):
        return f'{self.nome} {self.sobrenome}'
