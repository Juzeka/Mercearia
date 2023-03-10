
# Teste para vaga back-end

API de gerenciamento de um pequeno mercadinho.

## Visualização com Swagger
![Visualização](https://github.com/Juzeka/Mercearia/blob/master/swagger.png?raw=true)
## Relacionamento

![Relacionamento](https://github.com/Juzeka/Mercearia/blob/master/relacionamento.png?raw=true)


## Distribuição de pastas

- A distribuição é constituida com as apps no diretório apps e seu fluxo de estruturação em um app fica: factories, migrations, models, serializes, services e views.
- A nomeação dos arquivos seguem o mesmo nome do model.
- O diretório tests seguem a mesma lógica de apps.

![Pastas](https://github.com/Juzeka/Mercearia/blob/master/ordenacao.png?raw=true)

## Folha do Relatório
- Relatório diário de fechamento de caixa:
![Visualização](https://github.com/Juzeka/Mercearia/blob/master/relatorio.png?raw=true)

## Dependências extras utilizadas

### Visualização dos endpoints
- [**DRF spectacular**](https://drf-spectacular.readthedocs.io/en/latest/readme.html#installation)
### API
- [**Django REST Framework**](https://www.django-rest-framework.org/#installation)
- [**Python Decouple**](https://pypi.org/project/python-decouple/)
### Testes
- [**Parameterized**](https://pypi.org/project/parameterized/)
- [**Django Factory Boy**](https://pypi.org/project/django-factory_boy/)
### Converter HTML em PDF
- [**Weasyprint**](https://pypi.org/project/weasyprint/)
### Depuração
- [**IPython pdb**](https://pypi.org/project/ipdb/)
### Estilização
- [**Bootstrap 5**](https://getbootstrap.com/docs/5.0/getting-started/introduction/)
###

## Instalação

Para a Instalação execute os seguintes comandos no terminal.

- Clone o projeto em:
```bash
git clone https://github.com/Juzeka/Mercearia.git
```
Na pasta do projeto:
- Criação do ambiente virtual:
```bash
python3 -m venv venv
```
- Ativando o ambiente:
```bash
. venv/bin/activate
```

- Instalação das dependências:
```bash
pip install -r requirements.txt
```

### Criação das variáveis de ambiente
Crie um arquivo .env na pasta do projeto (onde o arquivo manage.py se encontra) e no terminal execute:

- Execute o comando:
```bash
python3
```

- Entre com:
```bash
from django.core.management.utils import get_random_secret_key

print(get_random_secret_key())
```
com a chave exibida pelo print cole no arquivo .env:
```bash
SECRET_KEY = 'chave gerada aqui!'
DEBUG = True
```


## Rodando o projeto

- Rode as makemigrations:
```bash
python3 manage.py makemigrations
```
- Rode as migrations:
```bash
python3 manage.py migrate
```
- Rode o servidor:
```bash
python3 manage.py runserver
```
## Rodando os testes

Para rodar os testes, rode o seguinte comando:

```bash
  python3 manage.py test tests
```
### Criar um caixa com vendas e sangrias
```bash
  python3 manage.py criar_caixa_com_vendas_e_sangrias
```
