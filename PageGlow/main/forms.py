from django import forms
from django.core.validators import MinLengthValidator

from django_ckeditor_5.widgets import CKEditor5Widget
from .models import *


class AddPostForm(forms.ModelForm):
    cat = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label='Не выбрано',
        label='Категория',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    content = forms.CharField(
        label='Статья',
        widget=CKEditor5Widget(config_name='default'),
        initial='<h1></h1>'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["content"].required = False

    class Meta:
        model = Post
        fields = [ 'content', 'is_published', 'cat', 'tags']
        widgets = {
            'photo': forms.ClearableFileInput(attrs={'class':'form-control'}),
            'tags': forms.SelectMultiple(attrs={'class':'form-control'}),
            'is_published': forms.CheckboxInput(attrs={'class':'form-checkbox'})
        }

    def clean_content(self):
        content = self.cleaned_data['content']
        # Проверяем наличие заголовка
        if content and not ('<h1>' in content or '<h2>' in content):
            content = '<h1>Заголовок</h1>' + content
        return content

class UploadFileForm(forms.Form):
    file = forms.FileField(label='Файл',widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 1, 'class': "form-control",}),
        }