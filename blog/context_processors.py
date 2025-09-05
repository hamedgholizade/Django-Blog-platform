from blog.models.post import Post


def session_recent_posts(request):
    recent_posts = request.session.get('history', [])
    recent_posts = Post.objects.filter(slug__in=recent_posts, status="C")[::-1]
    return {'recent_posts': recent_posts}

def cookie_last_viewed_post(request):
    last_viewed_post = None
    post_slug = request.COOKIES.get('last_viewed_post')
    if post_slug:
        try:
            last_viewed_post = Post.objects.get(slug=post_slug)
        except Post.DoesNotExist:
            pass
    return {"last_viewed_post": last_viewed_post}
