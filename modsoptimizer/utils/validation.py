from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


def validate_weekly_schedule(value):
    if len(value) != 192:
        raise ValidationError(
            _(f'`{value}` must be 192 characters long'),
            params={'value': value},
            code='invalid_length',
        )
    if not all(char in ('X', '0') for char in value):
        raise ValidationError(
            _(f'`{value}` must only contain X and O'),
            params={'value': value},
            code='invalid_value',
        )


def validate_exam_schedule(value):
    if len(value) != 38:
        raise ValidationError(
            _(f'`{value}` must be 38 characters long'),
            params={'value': value},
            code='invalid_length'
        )
    day, month, year, time = value[:2], value[2:4], value[4:6], value[6:]
    try:
        day, month, year = int(day), int(month), int(year)
        if not (1 <= day <= 31 and 1 <= month <= 12 and 0 <= year <= 99):
            raise ValidationError(
                _(f'`{value[:6]}` (first 6 chars) must be valid DDMMYY'),
                params={'value': value},
                code='invalid_format'
            )
    except ValueError:
        raise ValidationError(
            _(f'`{value[:6]}` (first 6 chars) must be in the format DDMMYY'),
            params={'value': value},
            code='invalid_format'
        )
    if not all(char in ('X', '0') for char in time):
        raise ValidationError(
            _(f'`{value}` (last 32 chars) must only contain X and O'),
            params={'value': value},
            code='invalid_value',
        )


validate_index = RegexValidator(
    regex=r'^\d{5}$',
    message=_('The value must be 5 numeric digits.'),
    code='invalid_format'
)
