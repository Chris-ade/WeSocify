from django import forms
from .models import *
from django.core.exceptions import ValidationError

class PostForm(forms.ModelForm):
  text = forms.CharField(max_length=500, widget=forms.Textarea)
  
  class Meta:
    model = Feed
    fields = ('text',)

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text']
        labels = {
            'choice_text': 'Choice'
        }

ChoiceFormSet = forms.formset_factory(ChoiceForm, extra=4)

class ImageForm(forms.ModelForm):
  image = forms.ImageField(required=False, label='Image')
  
  class Meta:
    model = FeedMedia
    fields = ('image',)