from django import forms
from django.utils.translation import ugettext as _

class SeparateMessagingServicesForm(forms.Form):
    event = forms.RegexField('\d+', widget=forms.HiddenInput)
    twitter = forms.CharField(label=_('Twitter'), max_length=140,
                              widget=forms.Textarea())

# from django.utils.translation import ugettext as _
# from django.core.exceptions import ValidationError
# from django import forms
# from django.forms.widgets import HiddenInput
# from django.core.files.images import get_image_dimensions

# from models import CinemaClubEvent, TemporaryImage, \
#     IMG_MIN_SIZE, IMG_MAX_SIZE

# class CinemaClubEventForm(forms.ModelForm):
#     class Meta:
#         model = CinemaClubEvent
#         fields = ('organizer', 'name', 'short_description',
#                   'description', 'starts_at', 'ends_at',)

# class TemporaryImageForm(forms.ModelForm):
#     class Meta:
#         model = TemporaryImage
#         fields = ('image',)

#     def clean(self, *args, **kwargs):
#         cleaned_data = super(TemporaryImageForm, self).clean(*args, **kwargs)

#         width, height = get_image_dimensions(cleaned_data['image'])
#         if not (IMG_MIN_SIZE <= width <= IMG_MAX_SIZE) or \
#                 not (IMG_MIN_SIZE <= height <= IMG_MAX_SIZE):
#             raise ValidationError('The image wigth and heigh must not exceed 300 and 1024')

#         return cleaned_data

# class CropImageForm(forms.Form):
#     x1 = forms.IntegerField(widget=HiddenInput())
#     x2 = forms.IntegerField(widget=HiddenInput())
#     y1 = forms.IntegerField(widget=HiddenInput())
#     y2 = forms.IntegerField(widget=HiddenInput())

#     def __init__(self, width, height, *args, **kwargs):
#         self._width = width
#         self._height = height
#         super(CropImageForm, self).__init__(*args, **kwargs)

#     def clean(self, *args, **kwargs):
#         cleaned_data = super(CropImageForm, self).clean(*args, **kwargs)

#         x2 = cleaned_data['x2']
#         y2 = cleaned_data['y2']
#         new_width = x2 - cleaned_data['x1']
#         new_height = y2 - cleaned_data['y1']

#         if new_width > self._width:
#             raise ValidationError(_('The selection width exceeds the original width.'))
#         if new_height > self._height:
#             raise ValidationError(_('The selection height exceeds the original height.'))
#         if x2 > self._width or y2 > self._height:
#             raise ValidationError(_('The selection doen\'t lie inside the image area.'))

#         return cleaned_data


# class CropImageForm(forms.Form):
#     def __init__(self, width, height, *args, **kwargs):
#         self._width = width
#         self._height = height
#         super(CropImageForm, self).__init__(*args, **kwargs)
