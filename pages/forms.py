from django import forms
from .models import ItemStatus


class IndexForm(forms.Form):

    name__contains = forms.CharField(label='Name',
                                     max_length=100,
                                     required=False)
    status = forms.ModelChoiceField(queryset=ItemStatus.objects.all(),
                                    required=False)
