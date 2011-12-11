from django.db import models
from django import forms


class CharFieldWithTextarea(models.CharField):
    def formfield(self, **kwargs):
        kwargs["widget"] = forms.Textarea(attrs={'rows': 3})
        return super(CharFieldWithTextarea, self).formfield(**kwargs)

from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^cinemaclubs\.fields\.CharFieldWithTextarea"])
