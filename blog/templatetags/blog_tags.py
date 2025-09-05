from django import template
from django.db.models import Avg

from blog.models.post import Post
from blog.models.user import User


register = template.Library()

@register.simple_tag(name='last_recent_posts')
def last_recent_posts(count=3):
    try:
        count = int(count)
    except (ValueError, TypeError):
        count = 3
    return Post.objects.filter(status='C').order_by('-published_date')[:count]


@register.simple_tag(name='top_authors')
def top_authors(count=3):
    try:
        count = int(count)
    except (ValueError, TypeError):
        count = 3
    return User.objects.filter(user_role="W") \
        .annotate(avg_visits=Avg('post__visit_count')) \
        .order_by('-avg_visits')[:count]





