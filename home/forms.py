from django import forms
from .models import MyFormModel

class MyForm(forms.ModelForm):
    class Meta:
        model = MyFormModel
        fields = '__all__'