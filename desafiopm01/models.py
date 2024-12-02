from django.db import models

class Itens(models.Model):
    # Informações da licitação
    descricao_licitacao = models.TextField()  
    modalidade = models.CharField(max_length=100)  
    comprador = models.CharField(max_length=100)  
    
    # Informações dos itens da licitação
    descricao_item = models.TextField()  
    unidade = models.CharField(max_length=100)  
    quantidade = models.PositiveIntegerField()  
    valor = models.DecimalField(max_digits=10, decimal_places=2)  

    def __str__(self):
        return f'Licitação: {self.descricao_licitacao} - Item: {self.descricao_item}'
