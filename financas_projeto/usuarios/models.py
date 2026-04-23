from django.db import models

class Usuario(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    email = models.CharField(max_length=150)
    senha = models.CharField(max_length=255)
    cpf = models.CharField(max_length=11)

    class Meta:
        db_table = 'usuarios'

        

class Projeto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=300)
    data_inicio = models.DateField()
    data_fim = models.DateField()
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    class Meta:
        db_table = 'projetos'

    def __str__(self):
        return self.nome