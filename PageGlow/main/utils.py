from PageGlow import settings

menu = [
    {'title': "Написать статью", 'url_name': 'addpage'},
    {'title': "О сайте", 'url_name': 'about'},
    {'title': "Контакты", 'url_name': 'contact'},
]



class DataMixin:
    paginate_by = 20
    title_page = None
    cat_selected = None
    extra_context = {
        'default_image': settings.DEFAULT_USER_IMAGE,
    }

    def __init__(self):
        if self.title_page:
            self.extra_context['title'] = self.title_page

        if self.cat_selected is not None:
            self.extra_context['cat_selected'] = self.cat_selected


    def get_mixin_context(self, context, **kwargs):
        context['cat_selected'] = None
        context.update(kwargs)
        return context