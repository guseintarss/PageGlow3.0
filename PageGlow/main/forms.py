from django import forms
from django.core.validators import MinLengthValidator

from ckeditor.widgets import CKEditorWidget
from markdown import markdown as md
from .models import *


class AddPostForm(forms.ModelForm):
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label='Не выбрано', label='Категория', widget=forms.Select(attrs={'class': 'form-select'}))
    content = forms.CharField(label='Текст', widget=CKEditorWidget(config_name='default'))

    class Meta:
        model = Post
        fields = ['title', 'content', 'photo', 'is_published', 'cat', 'tags']
        widgets = {
            'content': CKEditorWidget(config_name='default', attrs={'rows': 20, 'class': 'form-control', 'id': 'ckeditor-field'}),
            # 'content_markdawn': forms.Textarea(attrs={'rows': 20,'class':'form-control', 'id': 'markdown-field', 'style': 'display: none;'}),
            # 'is_published': forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'photo': forms.ClearableFileInput(attrs={'class':'form-control'}),
            'tags': forms.SelectMultiple(attrs={'class':'form-control'}),
        }
        label = {
            'content': 'Текст'
        }
    def clean_title(self):
        title = self.cleaned_data['title']
        return title

    def clean_content(self):
        content = self.cleaned_data.get('content')
        try:
            md(content)  # Проверка на валидность Markdown
        except:
            raise forms.ValidationError("Некорректный Markdown-синтаксис")
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