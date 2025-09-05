from django import template
from tag.models import Tag
from blog.models.post import Post


register = template.Library()

@register.simple_tag(name="posts_tags")
def posts_tags():
    tags = Tag.objects.all()
    posts = Post.objects.filter(status='C')
    tag_dict = {}
    for tag in tags:
        tag_dict[tag] = posts.filter(tag__name=tag.name).count()
    return tag_dict
