from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.contrib.auth.password_validation import MinimumLengthValidator, NumericPasswordValidator

class CustomMinimumLengthValidator(MinimumLengthValidator):
    def get_help_text(self):
        return _("Su contraseña debe contener al menos %(min_length)d caracteres." % {'min_length': self.min_length})

class CustomNumericPasswordValidator(NumericPasswordValidator):
    def get_help_text(self):
        return _("Su contraseña no puede ser completamente numérica.")
