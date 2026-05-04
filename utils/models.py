from django.db import models
from django.utils.text import slugify

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        abstract = True

class CommonModel(BaseModel):
    priority = models.PositiveIntegerField(default=0)
    slug = models.SlugField(blank=True, unique=True, db_index=True) # Added unique=True

    def save(self, *args, **kwargs):
        if not self.slug and hasattr(self, 'name'):
            self.slug = slugify(self.name) # Use Django's built-in slugify
        super().save(*args, **kwargs)

    class Meta:
        abstract = True