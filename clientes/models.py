from django.db import models

class Cliente(models.Model):
    cpf_cliente = models.CharField(max_length=14, primary_key=True)
    nome_completo = models.CharField(max_length=100)
    data_nascimento = models.DateField()
    endereco = models.CharField(max_length=100)
    numero = models.CharField(max_length=10)
    cep = models.CharField(max_length=9)
    cidade = models.CharField(max_length=50)
    uf = models.CharField(max_length=2)
    complemento = models.CharField(max_length=100, blank=True, null=True)
    telefone = models.CharField(max_length=15)
    celular = models.CharField(max_length=15)
    possui_reserva = models.BooleanField(default=False)
    senha = models.CharField(max_length=50, blank=True, null=True, verbose_name="Senha de acesso")
    
    def __str__(self):
        return f"{self.nome_completo} - {self.cpf_cliente}"
