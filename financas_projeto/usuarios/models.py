from django.db import models

class Usuario(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    email = models.CharField(max_length=150)
    senha = models.CharField(max_length=255)
    cpf = models.CharField(max_length=11)

    class Meta:
        db_table = 'Usuario'