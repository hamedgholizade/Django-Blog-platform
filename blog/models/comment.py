from django.db import models
from base.models import BaseModel
from blog.models import User, Post


class CommentQuerySet(models.QuerySet):
    def show_approved(self):
        return self.filter(is_shown = True)
    
    def approve(self):
        return self.update(is_shown = True)
    
    def hide(self):
        return self.update(is_shown = False)


class Comment(BaseModel):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    is_shown = models.BooleanField(default=False)

    objects = CommentQuerySet.as_manager()
    class Meta:
        permissions = [
            ("approve_comment", "Can approve comment"),
            ("hide_comment", "Can hide comment"),
        ]

    def approve_comment(self):
        self.is_shown = True
        self.save()

    def hide_comment(self):
        self.is_shown = False
        self.save()

    def __str__(self):
        return f"{self.user.username} on {self.post.title}"
