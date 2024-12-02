
# Desafio Django - Scraping e Armazenamento no Banco de Dados

Este projeto utiliza Django para realizar scraping de editais de licitação através da API do portal PNCP (Sistema de Compras Governamentais) e armazena os dados no banco de dados SQLite.

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
python -m venv env
```

Ative o ambiente virtual:

- **Windows**:
  ```bash
  .\env\Scripts\activate
  ```

- **Linux/macOS**:
  ```bash
  source env/bin/activate
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
python manage.py <nome_do_comando>
```

O nome do comando é o nome da classe dentro de `scraping_app/management/commands/`, geralmente algo como `scrape_edital.py` ou o que você escolheu ao implementar a função `BaseCommand`.

### 8. Testando a Aplicação

Depois de rodar o scraping, os dados serão armazenados na tabela `ServicoSetop` do banco de dados. Você pode verificar os dados no Django Admin ou usar o shell do Django:

```bash
python manage.py shell
```

No shell interativo, você pode consultar os dados:

```python
from scraping_app.models import ServicoSetop
ServicoSetop.objects.all()
```

## Estrutura do Projeto

O projeto tem a seguinte estrutura de diretórios:

```
projeto/
│
├── manage.py              # Script principal para rodar o Django
├── scraping_app/          # Aplicação de scraping
│   ├── management/
│   │   └── commands/      # Comandos personalizados de scraping
│   ├── models.py          # Modelos do banco de dados
│   ├── views.py           # Visões da aplicação
│   ├── urls.py            # URLs da aplicação
│   └── admin.py           # Configurações do admin do Django
│
├── requirements.txt       # Dependências do projeto
└── db.sqlite3             # Banco de dados SQLite (gerado automaticamente pelo Django)
```

## Contribuindo

1. Faça um fork deste repositório.
2. Crie uma branch para suas mudanças (`git checkout -b feature/nome-da-sua-feature`).
3. Faça as alterações necessárias e commit (`git commit -am 'Adicionando nova funcionalidade'`).
4. Faça o push para a sua branch (`git push origin feature/nome-da-sua-feature`).
5. Abra um pull request.

## Licença

Este projeto é licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para mais detalhes.
