from django.db import models


# Create your models here.
class BaseModel(models.Model):
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def soft_delete(self):
        self.is_deleted = True
        self.save()

    def hard_delete(self):
        super().delete()
        