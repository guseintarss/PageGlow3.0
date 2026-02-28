from django.contrib.syndication.views import Feed
from django.urls import reverse
from .models import Post


class LatestPostsFeed(Feed):
    title = "PageGlow - Новые статьи"
    link = "/"
    description = "Последние статьи на PageGlow"

    def items(self):
        return Post.published.order_by('-time_create')[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content[:300] + '...' if len(item.content) > 300 else item.content

    def item_link(self, item):
        return item.get_absolute_url()

    def item_pubdate(self, item):
        return item.time_create

    def item_author_name(self, item):
        return item.author.username if item.author else 'Аноним'
