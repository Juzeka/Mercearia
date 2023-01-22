from django import template
from decimal import Decimal


register = template.Library()

@register.filter
def parse_for_reais(value:Decimal):
    if value is None:
        return '-'

    return 'R$ {:,.2f}'.format(value).replace(',', 'X').replace(
        '.', ','
    ).replace('X', '.')

@register.filter
def zeros_esquerda(value):
    value = str(value) if value != 0 else value

    if len(value) == 4:
        value = f'0{value}'
    elif len(value) == 3:
        value = f'00{value}'
    elif len(value) == 2:
        value = f'000{value}'
    elif len(value) == 1:
        value = f'0000{value}'
    else:
        value = f'0000{value}'

    return value
