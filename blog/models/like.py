from django.db import models
from blog.models.user import User
from blog.models.post import Post
from base.models import BaseModel


class Like(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"{self.user.username} liked {self.post.title}"
