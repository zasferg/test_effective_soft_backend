import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_russian_characters(value):
    if not re.match(r"^[а-яА-ЯёЁ0-9\s]+$", value):
        raise ValidationError(
            _("Поле %(value)s должно содержать только русские буквы и цифры."),
            params={"value": value},
        )
