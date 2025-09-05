from django.db import models
from django.utils.text import slugify

from base.models import BaseModel
from blog.models import User
from tag.models import Tag


class Post(BaseModel):
    POST_STATUS_PENDING = "P"
    POST_STATUS_CONFIRMED = "C"
    POST_STATUS_REFUSED = "R"
    POST_STATUS_HIDDEN = "H"
    POST_STATUS_CHOICES = [
        (POST_STATUS_PENDING, "Pending"),
        (POST_STATUS_CONFIRMED, "Confirmed"),
        (POST_STATUS_REFUSED, "Refused"),
        (POST_STATUS_HIDDEN, "Hidden"),
    ]
    author = models.ForeignKey(to=User, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=255, unique=True)
    image = models.ImageField(upload_to="blog_photoes/", null=True, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    content = models.TextField()
    status = models.CharField(
        max_length=1, choices=POST_STATUS_CHOICES, default=POST_STATUS_PENDING
    )
    tag = models.ManyToManyField(Tag)
    likes = models.ManyToManyField(User, related_name='post_likes', blank=True)
    like_count = models.IntegerField(default=0)
    visit_count = models.IntegerField(default=0)
    published_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        permissions = [
            ("approve_post", "Can approve post"),
        ]

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} by {self.author.username}"
