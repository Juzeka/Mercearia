
# Teste para vaga back-end

API de gerenciamento de um pequeno mercadinho.



## Relacionamento

![Relacionamento](https://github.com/Juzeka/Mercearia/blob/master/relacionamento.png?raw=true)


## Dependências extras utilizadas

### API
- **Django REST Framework**
- **Python Decouple**
### Testes
- **Parameterized**
- **Django Factory Boy**
### Converter HTML em PDF
- **Weasyprint**
### Depuração
- **IPython pdb**
###

## Instalação

Para a Instalação execute os seguintes comandos no terminal.

```bash
Clone o projeto em:
    https://github.com/Juzeka/Mercearia.git
Na pasta do projeto:
    - Criação do ambiente virtual:
        python3 -m venv venv
    - Ativando o ambiente:
        . venv/bin/activate
    - Instalação das dependências:
        pip install -r requirements.txt
```

### Criação das variáveis de ambiente
Crie um arquivo .env na pasta do projeto (onde o arquivo manage.py se encontra) e no terminal execute:
```bash
Execute o comando:
    python3 manage.py shell
Entre com:    
    from django.core.management.utils import get_random_secret_key

    print(get_random_secret_key())
```
com a chave exibida pelo print cole no arquivo .env:
```bash
SECRET_KEY = 'chave gerada aqui!'
DEBUG = True
```

## Rodando o projeto


```bash
Rode as makemigration:
    python3 manage.py makemigration
Rode as migrations:
    python3 manage.py migrate
Instalação das dependências:
    pip install -r requirements.txt
Rode o servidor:
    python3 manage.py runserver
```
## Rodando os testes

Para rodar os testes, rode o seguinte comando:

```bash
  python3 manage.py test tests
```

