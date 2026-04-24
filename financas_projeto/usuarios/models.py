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
    


class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20)

    class Meta:
        db_table = 'categorias'



class TipoDespesa(models.Model):
    nome = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    class Meta:
        db_table = 'tipos_despesa'



class Despesa(models.Model):
    descricao = models.CharField(max_length=200)
    valor_orcado = models.FloatField()
    valor_realizado = models.FloatField()

    data = models.DateField()

    tipo = models.ForeignKey('TipoDespesa', on_delete=models.CASCADE)
    projeto = models.ForeignKey('Projeto', on_delete=models.CASCADE)

    class Meta:
        db_table = 'despesas'