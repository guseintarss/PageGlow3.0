from PageGlow import settings

menu = [
    {'title': "Написать статью", 'url_name': 'addpage'},
    {'title': "О сайте", 'url_name': 'about'},
]



class DataMixin:
    paginate_by = 20
    title_page = None
    cat_selected = None

    def get_extra_context(self):
        """Возвращает дополнительный контекст с базовыми значениями."""
        extra = {
            'default_image': settings.DEFAULT_USER_IMAGE,
        }
        # Используем getattr с дефолтным значением, чтобы избежать проблем с ORM
        title = getattr(self, 'title_page', None)
        if title:
            extra['title'] = title

        cat_selected = getattr(self, 'cat_selected', None)
        if cat_selected is not None:
            extra['cat_selected'] = cat_selected
        return extra

    def get_mixin_context(self, context, **kwargs):
        """Добавляет метаданные и другой контекст в словарь контекста."""
        # Обновляем контекст базовыми значениями
        context.update(self.get_extra_context())

        # Добавляем meta-теги, если объект поддерживает as_meta
        if hasattr(self, 'object') and self.object and hasattr(self.object, 'as_meta'):
            try:
                if hasattr(self, 'request'):
                    context['meta'] = self.object.as_meta(self.request)
                else:
                    # Если request недоступен, создаём meta без него
                    from meta.views import Meta
                    context['meta'] = Meta(
                        title=getattr(self.object, 'title', 'Без названия'),
                        description=getattr(self.object, 'content', '')[:200],
                    )
            except Exception as e:
                import logging
                logger = logging.getLogger(__name__)
                logger.warning(f"Ошибка генерации meta-тегов: {e}")
                context['meta'] = None
        else:
            context['meta'] = None  # Явно задаём None, если метаданные недоступны

        # Добавляем дополнительные параметры из kwargs
        context.update(kwargs)
        return context

    def get_context_data(self, **kwargs):
        """Переопределяем get_context_data для интеграции миксина."""
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, **kwargs)

