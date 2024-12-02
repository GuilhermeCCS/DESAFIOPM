# Desafio Django - Scraping e Armazenamento no Banco de Dados

Este projeto utiliza Django para realizar scraping de editais de licitação através da API do portal **PNCP (Sistema de Compras Governamentais)** e armazena os dados no banco de dados SQLite.

## Justificativa pela Escolha da Fonte de Dados: PNCP

Entre as três opções de fontes de dados fornecidas (SETOP, CAIXA e PNCP), a **PNCP** foi escolhida para este projeto pelas seguintes razões:

1. **Amplo Conjunto de Dados**: O PNCP oferece uma vasta quantidade de dados atualizados sobre editais e licitações, abrangendo uma grande variedade de informações de diferentes órgãos públicos. Isso permite um conjunto de dados mais robusto e completo.

2. **Estrutura de Dados Acessível**: O portal PNCP disponibiliza informações de maneira mais organizada e estruturada, facilitando o processo de raspagem com ferramentas como BeautifulSoup e Requests, ao contrário de fontes como a SETOP, que exigem extração de dados a partir de arquivos de planilhas, o que demandaria mais processamento.

3. **Relevância e Atualizações Frequentes**: O PNCP é constantemente atualizado e centraliza dados de licitações de diversas entidades governamentais. Isso garante que os dados extraídos são relevantes e em tempo real, permitindo que a aplicação se mantenha útil e atualizada.

Dessa forma, a escolha do **PNCP** oferece maior flexibilidade e escalabilidade ao projeto, com dados acessíveis, estruturados e de fácil raspagem.

## Requisitos

Antes de começar, certifique-se de que você tem os seguintes pré-requisitos instalados:

- [Python 3.8+](https://www.python.org/downloads/)
- [Django 4.x](https://www.djangoproject.com/download/)
- [Pip](https://pip.pypa.io/en/stable/)
- [Requests](https://requests.readthedocs.io/en/latest/)

## Como Rodar o Projeto

### 1. Clonando o Repositório

Primeiro, clone o repositório para a sua máquina local:

```bash
git clone https://github.com/usuario/repositorio.git
cd repositorio
```

### 2. Criando e Ativando o Ambiente Virtual

Crie um ambiente virtual para isolar as dependências do projeto:

```bash
python -m venv venv
```

Ative o ambiente virtual:

- **Windows**:
  ```bash
  .\venv\Scripts\activate
  ```

- **Linux/macOS**:
  ```bash
  source venv/bin/activate
  ```

### 3. Instalando as Dependências

Instale as dependências do projeto listadas no `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 4. Configurando o Banco de Dados

O projeto usa o SQLite como banco de dados. Para configurar o banco de dados e aplicar as migrações:

```bash
python manage.py migrate
```

### 5. Criando o Superusuário (opcional)

Se você deseja acessar o painel de administração do Django, crie um superusuário:

```bash
python manage.py createsuperuser
```

Siga as instruções para definir o nome de usuário, e-mail e senha.

### 6. Rodando o Servidor

Agora você pode rodar o servidor de desenvolvimento do Django:

```bash
python manage.py runserver
```

Abra o navegador e acesse `http://127.0.0.1:8000/` para visualizar a aplicação.

### 7. Executando o Scraping

Para rodar o comando de scraping que irá buscar os dados da API do PNCP e salvar no banco de dados, use o seguinte comando:

```bash
python manage.py iniciar_projeto
```

O nome do comando é o nome da classe dentro de `scraping_app/management/commands/`, geralmente algo como `scrape_edital.py` ou o que você escolheu ao implementar a função `BaseCommand`.