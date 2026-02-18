from .models import Post

def sidebar_context(request):
    return {
        'sidebar_new_posts': Post.objects.filter(
            is_published=True
        ).order_by('-time_create')[:5] 
    }
