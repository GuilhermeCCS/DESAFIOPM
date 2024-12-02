import requests
from django.core.management.base import BaseCommand
from desafiopm01.models import Itens  
from datetime import datetime
from django.utils import timezone

# Definir URL e cabeçalhos
URL = "https://pncp.gov.br/api/search/"
HEADERS = {
    "sec-ch-ua-platform": '',
    "Referer": "",
    "User-Agent": '',
}

params = {
    "tipos_documento": "edital",
    "ordenacao": "-data",
    "pagina": "1",
    "tam_pagina": "10",
    "status": "recebendo_proposta"
}

class Command(BaseCommand):
    help = 'Inicia o scraping e salva os dados no banco'

    def handle(self, *args, **kwargs):
        total_items = self.get_total_items()
        self.stdout.write(f"Total de itens: {total_items}")
        interval = 10 

        for i in range(interval):
            if i > 0:
                params['pagina'] = str(int(params['pagina']) + 1)
            
            self.stdout.write(f"Processando página {params['pagina']}...")
            response = requests.get(URL, headers=HEADERS, params=params)
            
            # Imprimir resposta completa da API para visualização
            data = response.json()
            print(data)  

            items_data = data.get('items', [])
            if not items_data:
                self.stdout.write(f"Nenhum item encontrado na página {params['pagina']}")
            
            for item_data in items_data:
                self.process_item(item_data)

    @staticmethod
    def get_total_items():
        response = requests.get(URL, headers=HEADERS, params=params)
        return response.json()['total']

    def process_item(self, item_data):
        licitacao_info = {
            'objeto': item_data.get('description', 'Descrição não disponível'),
            'modalidade': item_data.get('modalidade', 'Modalidade não informada'),
            'comprador': item_data.get('orgao_nome', 'Comprador não informado'),
        }

        # Verificar e processar itens dentro da licitação
        itens = item_data.get('itens', [])
        if not itens:
            self.stdout.write(f"Licitação '{licitacao_info['objeto']}' não possui itens.")

        # Processar cada item
        for item in itens:
            item_info = {
                'descricao': item.get('descricao', 'Descrição não disponível'),
                'unidade': item.get('unidade', 'Unidade não informada'),
                'quantidade': item.get('quantidade', 'Quantidade não informada'),
                'valor': item.get('valor', 'Valor não informado')
            }

            # Criar e salvar no banco o item da licitação
            Itens.objects.create(
                descricao_licitacao=licitacao_info['objeto'],
                modalidade=licitacao_info['modalidade'],
                comprador=licitacao_info['comprador'],
                descricao_item=item_info['descricao'],
                unidade=item_info['unidade'],
                quantidade=item_info['quantidade'],
                valor=item_info['valor'],
            )

            self.stdout.write(f"Licitação '{licitacao_info['objeto']}' e item '{item_info['descricao']}' salvos com sucesso!")

    def valid_date(self, date_value):
        if date_value == "Data não informada" or not date_value:
            return None
        try:
            naive_date = datetime.strptime(date_value, "%Y-%m-%dT%H:%M:%S.%f")
            aware_date = timezone.make_aware(naive_date, timezone.get_current_timezone())
            return aware_date
        except ValueError:
            return None
