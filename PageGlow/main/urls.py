from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
# router.register('post', views.ProjectViewset, basename='post')
# urlpatterns = router.urls


urlpatterns = [
    path('', views.MainHome.as_view(), name='home'),
    path('api/mymodel/', views.MyModelList.as_view(), name='mymodel-list'),
    path('admin/', admin.site.urls, name='admin'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('search/', views.Search.as_view(), name='search'),
    path('login/', views.login, name='login'),
    path('addpage/', views.AddPage.as_view(), name='addpage'),
    path('post/<slug:post_slug>/', views.ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>/', views.MainCategory.as_view(), name='category'),
    path('tag/<slug:tag_slug>/', views.TagPostList.as_view(), name='tag'),
    path('edit/<slug:slug>/', views.UpdatePage.as_view(), name='edit_page'),
    re_path(r'^.*$', views.react_app, name='react-app'),

]

