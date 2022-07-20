from email.policy import default
from pyexpat import model
from django.db import models
from setor.models import Setor

# Create your models here.

class Equipamento(models.Model):
    descricao = models.CharField(max_length=25, unique=True)
    valor_custo = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    qtd_estoque = models.IntegerField(default=0)
    setores = models.ManyToManyField(Setor, through='EquipamentoSetor')

    def __str__(self):
        return self.descricao

class EquipamentoSetor(models.Model):
    equipamento = models.ForeignKey(Equipamento, on_delete=models.CASCADE)
    setor = models.ForeignKey(Setor, on_delete=models.CASCADE)
    validade = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.equipamento.__str__()}_{self.setor.__str__()}'
        
