from django.db import models

class PersonCategory(models.Model):
    title_uz = models.CharField(max_length=100)
    title_ru = models.CharField(max_length=100, blank=True)
    title_en = models.CharField(max_length=100, blank=True)
    
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title_uz

class Person(models.Model):
    categories = models.ManyToManyField(PersonCategory, related_name='persons')
    
    image = models.ImageField(upload_to='persons/%Y/%m/')
    
    full_name_uz = models.CharField(max_length=255)
    full_name_ru = models.CharField(max_length=255, blank=True)
    full_name_en = models.CharField(max_length=255, blank=True)
    
    description_uz = models.TextField()
    description_ru = models.TextField(blank=True)
    description_en = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-id']

    def __str__(self):
        return self.full_name_uz