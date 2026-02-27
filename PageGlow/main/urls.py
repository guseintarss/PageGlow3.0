from django.contrib import admin
from django.urls import path

from . import views
from .feeds import LatestPostsFeed


urlpatterns = [
    path('', views.MainHome.as_view(), name='home'),
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
    path('ajax/like/', views.PostLikeAjaxView.as_view(), name='post_like_ajax'),
    path('ajax/favorite/', views.PostFavoriteAjaxView.as_view(), name='post_favorite_ajax'),
    path('ajax/add-comment/', views.AddCommentAjaxView.as_view(), name='add_comment_ajax'),
    path('ajax/delete-comment/', views.DeleteCommentAjaxView.as_view(), name='delete_comment_ajax'),
    path('upload/', views.CKEditorUploadView.as_view(), name='ckeditor_upload'),
    # Новые маршруты
    path('popular/', views.PopularPostsView.as_view(), name='popular'),
    path('feed/', views.SubscriptionFeedView.as_view(), name='subscription_feed'),
    path('ajax/subscribe/', views.SubscribeAuthorView.as_view(), name='subscribe_author'),
    path('ajax/notifications/', views.NotificationsView.as_view(), name='notifications'),
    path('ajax/notifications/read/', views.MarkNotificationsReadView.as_view(), name='mark_notifications_read'),
    path('rss/', LatestPostsFeed(), name='rss_feed'),
]

