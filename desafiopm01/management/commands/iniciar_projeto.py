import requests
from django.core.management.base import BaseCommand
from desafiopm01.models import Itens
from datetime import datetime
from django.utils import timezone
import time

URL = "https://pncp.gov.br/api/search/"
HEADERS = {
    "sec-ch-ua-platform": '',
    "Referer": "",
    "User-Agent": '',
}

params = {
    "q": "abc",
    "tipos_documento": "edital",
    "ordenacao": "-data",
    "pagina": "1",
    "tam_pagina": "10",
    "status": "encerradas",
}

class Command(BaseCommand):
    help = 'Inicia o scraping e salva os dados no banco de forma contínua com pausa de 1 minuto entre execuções'

    def handle(self, *args, **kwargs):
        pagina_atual = 1

        while True:
            self.stdout.write(f"Processando página {pagina_atual}...")
            params['pagina'] = str(pagina_atual)
            response = requests.get(URL, headers=HEADERS, params=params)

            if response.status_code != 200:
                self.stdout.write(f"Erro na requisição. Status: {response.status_code}")
                time.sleep(60)
                continue

            data = response.json()
            print("JSON retornado da API:", data)

            items_data = data.get('items', [])
            if not items_data:
                self.stdout.write(f"Nenhum item encontrado na página {pagina_atual}")
                time.sleep(60)
                continue

            for item_data in items_data:
                print("Dados completos de uma licitação:", item_data)
                self.process_item(item_data)

            pagina_atual += 1
            self.stdout.write("Aguardando 1 minuto para a próxima página...")
            time.sleep(60)

    def process_item(self, item_data):
        licitacao_info = {
            'objeto': item_data.get('description', 'Descrição não disponível'),
            'modalidade': item_data.get('modalidade_licitacao_nome', 'Modalidade não informada'), 
            'comprador': item_data.get('orgao_nome', 'Comprador não informado'),
            'orgao_cnpj': item_data.get('orgao_cnpj', 'CNPJ não informado'),
            'numero_sequencial': item_data.get('numero_sequencial', 'Número sequencial não informado'),
            'ano': item_data.get('ano', 'Ano não informado'),
        }

        print("Verificando a existência de itens nesta licitação...")

        if not licitacao_info['numero_sequencial'] or not licitacao_info['ano']:
            self.stdout.write(f"Licitação '{licitacao_info['objeto']}' não possui informações completas para acessar os itens.")
            return

        itens_url = f"https://pncp.gov.br/api/pncp/v1/orgaos/{licitacao_info['orgao_cnpj']}/compras/{licitacao_info['ano']}/{licitacao_info['numero_sequencial']}/itens?pagina=1&tamanhoPagina=5"
        response_itens = requests.get(itens_url, headers=HEADERS)

        if response_itens.status_code != 200:
            self.stdout.write(f"Erro ao acessar os itens da licitação '{licitacao_info['numero_sequencial']}'. Status: {response_itens.status_code}")
            return

        itens_data = response_itens.json()

        if isinstance(itens_data, list):
            print(f"Recebidos {len(itens_data)} itens para a licitação.")
        else:
            self.stdout.write(f"Erro: Estrutura de dados inesperada ao tentar acessar os itens.")
            return

        for item in itens_data:
            item_info = {
                'numero_item': item.get('numeroItem', 'Número do item não informado'),
                'descricao': item.get('descricao', 'Descrição não disponível'),
                'quantidade': item.get('quantidade', 'Quantidade não informada'),
                'valor_unitario_estimado': item.get('valorUnitarioEstimado', 'Valor unitário não informado'),
                'valor_total_estimado': item.get('valorTotal', 'Valor total não informado'),
                'unidade_medida': item.get('unidadeMedida', 'Unidade não informada')
            }

            Itens.objects.create(
                descricao_licitacao=licitacao_info['objeto'],
                modalidade=licitacao_info['modalidade'],  
                comprador=licitacao_info['comprador'],
                descricao_item=item_info['descricao'],
                unidade=item_info['unidade_medida'],
                quantidade=item_info['quantidade'],
                valor=item_info['valor_unitario_estimado'],
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