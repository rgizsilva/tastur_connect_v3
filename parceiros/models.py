import re
from django.db import models


class Parceiro(models.Model):
    cnpj = models.CharField(max_length=14, null=False, blank=False, default='00000000000000')
    nome_fantasia = models.CharField(max_length=100)
    data_entrada = models.DateField()
    endereco = models.CharField(max_length=100)
    numero = models.CharField(max_length=10)
    cep = models.CharField(max_length=9)
    cidade = models.CharField(max_length=50)
    uf = models.CharField(max_length=2)
    complemento = models.CharField(max_length=100, blank=True, null=True)
    telefone = models.CharField(max_length=15)
    celular = models.CharField(max_length=15)
    email = models.EmailField()

    def save(self, *args, **kwargs):
        self.cnpj = re.sub(r'\D', '', self.cnpj)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nome_fantasia} - {self.cnpj}"
