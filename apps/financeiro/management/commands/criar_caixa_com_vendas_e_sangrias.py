from django.core.management.base import BaseCommand
from apps.produtos.factories import (
    CategoriaFactory,
    ProdutoFactory,
    ProdutoOrigemFactory
)
from apps.financeiro.factories import (
    CaixaFactory,
    ItemVendaFactory,
    SangriaFactory,
    VendaFactory
)
from apps.financeiro.services import VendaServices
from datetime import datetime


class Command(BaseCommand):
    help = 'Criação de um caixa com vendas e sangrias'

    def handle(self, *args, **options):
        data = {
            'categoria': CategoriaFactory(),
            'valor': 10,
            'quantidade': 100
        }
        origem = ProdutoOrigemFactory(**data)

        data.update({'origem': origem})

        produto = ProdutoFactory(**data)
        caixa = CaixaFactory(valor_inicial=30.0, aberto=True)
        vendas = VendaFactory.create_batch(2, forma_pagamento='AB')
        sangrias = SangriaFactory.create_batch(2, valor=10.0)

        for venda in vendas:
            itens = ItemVendaFactory.create_batch(
                size=5,
                venda=venda,
                produto=produto,
                quantidade=2
            )

            venda.forma_pagamento = 'DI'
            venda.finalizada = True
            venda.save()

            caixa.vendas.add(venda)
            caixa.save()

            for item in itens:
                VendaServices(data={
                    'venda':venda.pk,
                    'produto': produto.pk,
                    'produto_origem': origem.pk,
                    'quantidade': item.quantidade
                }).atualizar_estoque(origem)

        for sangria in sangrias:
            caixa.sangrias.add(sangria)
            caixa.save()

        caixa.aberto = False
        caixa.fechado_em = datetime.now()
        caixa.save()
