from bleach import clean
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.views.generic.edit import FormMixin, DeleteView
from requests import Response
from bs4 import BeautifulSoup
from django.shortcuts import render

from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets, permissions
import math
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.uploadedfile import UploadedFile
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView
from django.contrib import messages

from PageGlow import settings
from main.serializers import PostSerializer
from .forms import AddPostForm, UploadFileForm, CommentForm
from .models import Post, Category, TagPost, UploadFiles
from .utils import DataMixin

# class ProjectViewset(viewsets.ViewSet):
#     permission_classes = [permissions.AllowAny]
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer


#     def list(self, request):
#         queryset = self.queryset
#         serializer = self.serializer_class(queryset, many=True)
#         return Response(serializer.data)

#     def create(self, request):
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=400)
        
#     def retrive(self, request, pk=None):
#         post = self.queryset.get(pk=pk)
#         serializer = self.serializer_class(post)
#         return Response(serializer.data)

#     def update(self, request, pk=None):
#         post = self.queryset.get(pk=pk)
#         serializer = self.serializer_class(post, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=400)       

#     def destro(self, request, pk=None):
#         post = self.queryset.get(pk=pk)
#         post.delete()
#         return Response(status=204)



class MainHome(DataMixin, ListView):
    template_name = 'main/index.html'
    context_object_name = 'posts'
    title_page = 'Главная страница'
    cat_selected = 0


    def get_queryset(self):
        return Post.published.all().select_related('cat', 'author')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context

def react_app(request):
    return render(request, 'home')

# class CustomSuccessMessageMixin:
#     @property
#     def success_msg(self):
#         return False
#
#     def form_valid(self, form):
#         messages.success(self.request, self.success_msg)
#         return super().form_valid(form)
#
#     def get_success_url(self):
#         return '%s?id=%s' % (self.success_url(), self.object.id)

class ShowPost(FormMixin, DataMixin, DetailView):
    template_name = 'main/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'
    form_class = CommentForm
    success_msg = 'Комментарий оставлен'

    def get_success_url(self, **kwargs):
        return reverse_lazy('post', kwargs={'post_slug': self.get_object().slug})

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.post = self.get_object()
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_object(self, queryset=None):
        post = get_object_or_404(Post.published, slug=self.kwargs[self.slug_url_kwarg])
        allowed_tags = [
            'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
            'ul', 'ol', 'li', 'strong', 'em', 'a', 'img',
            'blockquote', 'code', 'pre', 'i', 'span',
        ]

        post.content = clean(post.content, tags=allowed_tags)
        return post


@login_required
def about(request):
    context = {
        'default_image': settings.DEFAULT_USER_IMAGE,
    }
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            fp = UploadFiles(file=form.cleaned_data['file'])
            fp.save()
    else:
        form = UploadFileForm()
    return render(request, 'main/about.html', {'title' : 'О сайте', 'form': form, 'context': context})

def contact(request):
    return render(request, 'main/contact.html')

class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'main/addpage.html'
    title_page = 'Добавление статьи'

    def form_valid(self, form):
        html_content = form.cleaned_data['content']
        soup = BeautifulSoup(html_content, 'html.parser')
        heading = soup.find(['h1'])

        w = form.save(commit=False)
        w.author = self.request.user

        if heading:
            form.instance.title = heading.get_text(strip=True)
            heading.decompose()
            form.instance.content = str(soup)
        else:
            form.instance.title = 'Без заголовка'


        return super().form_valid(form)

class UpdatePage(DataMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'photo', 'is_published', 'cat']
    template_name = 'main/addpage.html'
    success_url = reverse_lazy('home')
    title_page = 'Редактирование статьи'

    def get_success_url(self, **kwargs):
        return reverse_lazy('post', kwargs={'post_slug': self.get_object().slug})

def login(request):
    return render(request, 'main/login.html')


class PostDeleteView(LoginRequiredMixin, DataMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('users:profile')

    def form_valid(self, form):
        print(f"Удален объект: {self.object}")
        return super().form_valid(form)

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

class MainCategory(DataMixin, ListView):
    template_name = 'main/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Post.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context["posts"][0].cat
        return self.get_mixin_context(context, title='Категория - ' + cat.name, cat_selected=cat.pk)


class MyModelList(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

def page_not_found(request, exception):
    return render(request, '404.html', status=404)

class TagPostList(DataMixin, ListView):
    template_name = 'main/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(context, title='Тег: ' + tag.tag)

    def get_queryset(self):
        return Post.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')


class Search(DataMixin, ListView):
    template_name = 'main/index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        query = self.request.GET.get('q', '')  # Получаем поисковый запрос (пустая строка, если нет)

        if query:
            # Ищем совпадение в title ИЛИ в content (без учёта регистра)
            search = Post.published.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query)
            )
        else:
            # Если запроса нет — возвращаем все опубликованные посты
            search = Post.published.all()

        return search


    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['q'] = self.request.GET.get('q')
        return context


class BaseView(View):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['new_posts'] = Post.objects.filter(status=Post.Status.PUBLISHED).order_by('-created_at')[:5]
        return context