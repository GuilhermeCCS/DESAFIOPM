from django.db import models

class Itens(models.Model):
    # Informações da licitação
    descricao_licitacao = models.TextField()  # Objeto/Descrição do edital
    modalidade = models.CharField(max_length=100)  # Modalidade da licitação
    comprador = models.CharField(max_length=100)  # Comprador da licitação
    
    # Informações dos itens da licitação
    descricao_item = models.TextField()  # Descrição do item
    unidade = models.CharField(max_length=100)  # Unidade de medida
    quantidade = models.PositiveIntegerField()  # Quantidade do item
    valor = models.DecimalField(max_digits=10, decimal_places=2)  # Valor do item

    def __str__(self):
        return f'Licitação: {self.descricao_licitacao} - Item: {self.descricao_item}'
