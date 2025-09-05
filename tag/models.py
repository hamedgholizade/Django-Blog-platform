from django.db import models
from django.utils.text import slugify
from base.models import BaseModel

class Tag(BaseModel):
    
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    description = models.TextField(null=True, blank=True)


    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Tag, self).save(*args, **kwargs)
