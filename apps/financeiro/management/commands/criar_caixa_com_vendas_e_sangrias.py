from django.core.management.base import BaseCommand
from apps.produtos.factories import CategoriaFactory, ProdutoFactory
from apps.financeiro.factories import (
    CaixaFactory,
    ItemVendaFactory,
    SangriaFactory,
    VendaFactory
)
from datetime import datetime


class Command(BaseCommand):
    help = 'Criação de um caixa com vendas e sangrias'

    def handle(self, *args, **options):
        produto = ProdutoFactory(
            categoria=CategoriaFactory(),
            valor=10,
            quantidade=100
        )
        caixa = CaixaFactory(valor_inicial=30.0, aberto=True)
        vendas = VendaFactory.create_batch(2, forma_pagamento='AB')
        sangrias = SangriaFactory.create_batch(2, valor=10.0)

        for venda in vendas:
            ItemVendaFactory.create_batch(
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

        for sangria in sangrias:
            caixa.sangrias.add(sangria)
            caixa.save()

        caixa.aberto = False
        caixa.fechado_em = datetime.now()
        caixa.save()
