# Generated by Django 4.1.5 on 2023-01-20 23:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import utilities.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('produtos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sangria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado_em', models.DateTimeField(auto_now=True, verbose_name='Criado em')),
                ('alterado_em', models.DateTimeField(auto_now_add=True, verbose_name='Alterado em')),
                ('valor', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Valor')),
                ('descricao', models.CharField(blank=True, max_length=200, null=True, verbose_name='Descrição')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Venda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado_em', models.DateTimeField(auto_now=True, verbose_name='Criado em')),
                ('alterado_em', models.DateTimeField(auto_now_add=True, verbose_name='Alterado em')),
                ('forma_pagamento', models.CharField(choices=[('DI', 'Dinheiro'), ('CD', 'Débito'), ('CC', 'Crédito')], default='DI', max_length=20)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ItemVenda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado_em', models.DateTimeField(auto_now=True, verbose_name='Criado em')),
                ('alterado_em', models.DateTimeField(auto_now_add=True, verbose_name='Alterado em')),
                ('quantidade', models.IntegerField(default=0, validators=[utilities.validators.numero_positivo], verbose_name='Quantidade')),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='item_venda_produto', to='produtos.produto', verbose_name='Produto da venda')),
                ('venda', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='item_venda_venda', to='financeiro.venda', verbose_name='Venda')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Caixa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aberto', models.BooleanField(auto_created=True, default=True, verbose_name='Aberto')),
                ('criado_em', models.DateTimeField(auto_now=True, verbose_name='Criado em')),
                ('alterado_em', models.DateTimeField(auto_now_add=True, verbose_name='Alterado em')),
                ('sangrias', models.ManyToManyField(blank=True, null=True, related_name='caixa_sangrias', to='financeiro.sangria', verbose_name='Sangrias')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
                ('vendas', models.ManyToManyField(blank=True, null=True, related_name='caixa_vendas', to='financeiro.venda', verbose_name='Vendas')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
