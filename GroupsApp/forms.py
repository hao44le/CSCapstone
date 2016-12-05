"""GroupsApp Forms

Created by Naman Patwari on 10/10/2016.
"""
from django import forms
from .models import Group

class GroupForm(forms.Form):
    name = forms.CharField(label='Name', max_length=30)
    description = forms.CharField(label='Description', max_length=300)
class CommentForm(forms.Form):
    comment = forms.CharField(label='Text', max_length=500)
class UpdateForm(forms.ModelForm):

    class Meta:
        model = Group
        fields = ('name', 'description')
        widgets = {
            'description': forms.Textarea()
        }
