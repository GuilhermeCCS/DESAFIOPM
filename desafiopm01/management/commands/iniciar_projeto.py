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
    "status": "encerrado",
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

                if not self.is_encerrado(item_data):
                    self.stdout.write(f"Licitação '{item_data.get('description')}' não está encerrada.")
                    continue

                licitacao_url = item_data.get('item_url')  
                if licitacao_url:
                    self.extract_and_save_licitacao_items(licitacao_url)

            pagina_atual += 1
            self.stdout.write("Aguardando 1 minuto para a próxima página...")
            time.sleep(60)

    def extract_and_save_licitacao_items(self, item_url):
        full_url = f"https://pncp.gov.br{item_url}"  
        licitacao_response = requests.get(full_url, headers=HEADERS)

        if licitacao_response.status_code != 200:
            self.stdout.write(f"Erro ao acessar os detalhes dos itens. Status: {licitacao_response.status_code}")
            return

        licitacao_data = licitacao_response.json()  
        itens = licitacao_data.get('itens', [])

        if not itens:
            self.stdout.write(f"Licitação não possui itens.")
            return

        for item in itens:
            item_info = {
                'descricao': item.get('descricao', 'Descrição não disponível'),
                'quantidade': item.get('quantidade', 'Quantidade não informada'),
                'valor_unitario': item.get('valor_unitario_estimado', 'Valor unitário não informado'),
                'valor_total': item.get('valor_total_estimado', 'Valor total não informado')
            }

            Itens.objects.create(
                descricao_licitacao=item_info['descricao'],  
                modalidade='',  
                comprador='',  
                descricao_item=item_info['descricao'],
                unidade='',  
                quantidade=item_info['quantidade'],
                valor=item_info['valor_unitario'],
            )

            self.stdout.write(f"Item '{item_info['descricao']}' salvo com sucesso!")

    def is_encerrado(self, item_data):
        status = item_data.get('status', '')
        if status == 'encerrado':
            return True

        data_encerramento = item_data.get('data_encerramento')
        if data_encerramento:
            data_encerramento = datetime.strptime(data_encerramento, "%Y-%m-%dT%H:%M:%S.%f")
            if data_encerramento < datetime.now():
                return True
        return False
