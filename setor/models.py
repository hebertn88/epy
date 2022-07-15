from django.db import models

# Create your models here.

class Setor(models.Model):
    descricao = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.descricao