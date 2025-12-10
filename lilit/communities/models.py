from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify

from lilit import settings



class Communities(models.Model):
    name = models.CharField(max_length=256, unique=True)
    slug = models.SlugField(blank=True)
    about = models.TextField(max_length=4096)
    themes = models.ManyToManyField('posts.Themes', related_name='communities_by_theme',)

    member=models.ManyToManyField(User, related_name='communities_of_member')

    is_creator=models.BooleanField(default=False)
    is_admin=models.BooleanField(default=False)
    is_redactor = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save( *args, **kwargs)

