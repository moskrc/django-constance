import os
from django.db import models
from django.core.exceptions import ImproperlyConfigured
from cryptography.fernet import Fernet, InvalidToken
from django.utils.translation import ugettext_lazy as _
from ... import settings
import logging

logger = logging.getLogger(__name__)

fernet_key = settings.ENCRYPTION_KEY

try:
    from picklefield import PickledObjectField
except ImportError:
    raise ImproperlyConfigured("Couldn't find the the 3rd party app "
                               "django-picklefield which is required for "
                               "the constance database backend.")

if not fernet_key:
    raise Exception('Environment variable CONSTANCE_ENCRYPTION_KEY must exist')


class EncryptedPickledObjectField(PickledObjectField):
    def __init__(self, *args, **kwargs):
        super(EncryptedPickledObjectField, self).__init__(*args, **kwargs)
        self.fernet = Fernet(fernet_key)

    def to_python(self, value):
        try:
            value = self.fernet.decrypt(value.encode())
        except InvalidToken as e:
            logger.critical(e)
            raise InvalidToken('The token is Invalid for the data in DB')

        return super(EncryptedPickledObjectField, self).to_python(value)

    def get_db_prep_value(self, value, connection=None, prepared=False):
        value = super(EncryptedPickledObjectField, self).get_db_prep_value(value, connection, prepared)
        return self.fernet.encrypt(value.encode())



class Constance(models.Model):
    key = models.CharField(max_length=255, unique=True)
    value = EncryptedPickledObjectField()

    class Meta:
        verbose_name = _('constance')
        verbose_name_plural = _('constances')
        db_table = 'constance_config'

    def __unicode__(self):
        return self.key
