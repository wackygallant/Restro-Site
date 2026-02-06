from django.db import models

from utils.models import CommonModel


class Chefs(CommonModel):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    bio = models.TextField()
    image = models.ImageField(upload_to='chefs/')

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'chef'
        verbose_name = 'Chef'
        verbose_name_plural = 'Chefs'


class Testimonials(CommonModel):
    name = models.CharField(max_length=100)
    review = models.TextField()
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    image = models.ImageField(upload_to='testimonials/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.rating}⭐"

    class Meta:
        db_table = 'testimonial'
        verbose_name = 'Testimonial'
        verbose_name_plural = 'Testimonials'