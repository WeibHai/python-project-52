from django.db import models as m
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Labels(m.Model):
    name = m.CharField(max_length=255, unique=True, verbose_name=_('Label name'))
    created_at = m.DateTimeField(auto_now_add=True, verbose_name=_('Created'))

    def __str__(self):
        return self.name
