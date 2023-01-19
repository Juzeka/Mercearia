from django.core.exceptions import ValidationError


def numero_positivo(value):
    if value < 0:
        raise ValidationError(
            ('Um número positivo é exigido.'),
            params={'value': value},
        )
