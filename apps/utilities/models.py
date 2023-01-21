from django.db import models


class CriadoAlteradoEm(models.Model):
    class Meta:
        abstract = True

    criado_em = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name='Criado em'
    )
    alterado_em = models.DateTimeField(
        auto_now=True,
        editable=False,
        verbose_name='Alterado em'
    )


class NomeDescricao(models.Model):
    class Meta:
        abstract = True

    nome = models.CharField(
        max_length=200,
        blank=False,
        null=False,
        verbose_name='Nome'
    )
    descricao = models.CharField(
        max_length=300,
        blank=True,
        null=True,
        verbose_name='Descrição'
    )

    def __str__(self):
        return self.nome
