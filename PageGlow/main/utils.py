from PageGlow import settings
import logging


menu = [
    {'title': "Написать статью", 'url_name': 'addpage'},
    {'title': "О сайте", 'url_name': 'about'},
]

logger = logging.getLogger(__name__)

class DataMixin:
    paginate_by = 20
    title_page = None
    cat_selected = None

    def get_extra_context(self):
        """Возвращает дополнительный контекст с базовыми значениями."""
        extra = {
            'default_image': settings.DEFAULT_USER_IMAGE,
            'menu': menu,  # Добавляем меню в контекст
        }

        # Устанавливаем заголовок
        if self.title_page:
            extra['title'] = self.title_page
        elif hasattr(self, 'object') and self.object:
            extra['title'] = getattr(self.object, 'title', 'Без названия')

        cat_selected = getattr(self, 'cat_selected', None)
        if cat_selected is not None:
            extra['cat_selected'] = cat_selected

        return extra

    def get_mixin_context(self, context, **kwargs):
        """Добавляет метаданные и другой контекст в словарь контекста."""
        context.update(self.get_extra_context())

        # Добавляем meta-теги, если объект поддерживает as_meta
        if hasattr(self, 'object') and self.object and hasattr(self.object, 'as_meta'):
            try:
                if hasattr(self, 'request'):
                    context['meta'] = self.object.as_meta(self.request)
                else:
                    from meta.views import Meta
                description = str(getattr(self.object, 'content', ''))[:200]
                context['meta'] = Meta(
                    title=getattr(self.object, 'title', 'Без названия'),
                    description=description,
                )
            except Exception as e:
                logger.warning(f"Ошибка генерации meta-тегов: {e}")
                context['meta'] = None
        else:
            context['meta'] = None

        context.update(kwargs)
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) if hasattr(super(), 'get_context_data') else kwargs.copy()

        # Инициализируем значения по умолчанию
        context['post_is_liked'] = False
        context['post_is_favorited'] = False
        context['number_of_likes'] = 0
        context['number_of_favorites'] = 0
        context['comments'] = []

        # Заполняем данные только если объект существует
        if hasattr(self, 'object') and self.object:
            if self.request.user.is_authenticated:
                context['post_is_liked'] = self.object.likes.filter(id=self.request.user.id).exists()
                context['post_is_favorited'] = self.object.favorites.filter(id=self.request.user.id).exists()

            context['number_of_likes'] = self.object.number_of_likes()
            context['number_of_favorites'] = self.object.number_of_favorites()
            context['comments'] = self.object.comments.filter(is_active=True)

        return self.get_mixin_context(context, **kwargs)
