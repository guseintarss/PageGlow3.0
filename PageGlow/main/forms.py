from django import forms
from django.core.validators import MinLengthValidator

from django_ckeditor_5.widgets import CKEditor5Widget
from markdown import markdown as md
from .models import *


class AddPostForm(forms.ModelForm):
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label='Не выбрано', label='Категория', widget=forms.Select(attrs={'class': 'form-select'}))
    content = forms.CharField(label='Контент', widget=CKEditor5Widget(config_name='default'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["content"].required = False

    class Meta:
        model = Post
        fields = ['title', 'content', 'photo', 'is_published', 'cat', 'tags']
        widgets = {
            'photo': forms.ClearableFileInput(attrs={'class':'form-control'}),
            'tags': forms.SelectMultiple(attrs={'class':'form-control'}),
        }
    def clean_title(self):
        title = self.cleaned_data['title']
        return title

class UploadFileForm(forms.Form):
    file = forms.FileField(label='Файл',widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 1, 'class': "form-control",}),
        }