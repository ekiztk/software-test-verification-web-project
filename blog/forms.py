from django import forms
from .models import ImageUploadModel

class ImageUploadForm(forms.ModelForm):
    low_h = forms.IntegerField(min_value=0, max_value=255,initial=0)
    low_v = forms.IntegerField(min_value=0, max_value=255,initial=0)
    low_s = forms.IntegerField(min_value=0, max_value=255,initial=199)
    high_h = forms.IntegerField(min_value=0, max_value=255,initial=180)
    high_v = forms.IntegerField(min_value=0, max_value=255,initial=50)
    high_s = forms.IntegerField(min_value=0, max_value=255,initial=255)

    class Meta:
        model = ImageUploadModel
        fields = ('image', "low_h", "low_v", "low_s", "high_h", "high_v", "high_s")