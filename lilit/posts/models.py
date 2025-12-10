import string
import random
from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse

from communities.models import Communities
from lilit import settings



def generate_random_string(length):
    characters = string.ascii_lowercase + string.digits
    result = ''.join(random.choice(characters) for _ in range(length))
    return result


class Themes(models.Model):
    theme = models.CharField(max_length=128)
    slug = models.SlugField(blank=True)

    def get_absolute_url(self):
        return reverse('posts_by_theme', kwargs={'slug':self.slug})

    def __str__(self):
        return self.theme

    def save(self, *args, **kwargs):
        self.slug = slugify(self.theme)
        return super().save( *args, **kwargs)


class Posts(models.Model):

    title = models.CharField(max_length=256, default='Without title')
    slug = models.SlugField(blank=True)
    content = models.TextField(max_length=4096)
    theme = models.ManyToManyField('posts.Themes', related_name='posts_by_theme')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts_of_author')
    community = models.ForeignKey(Communities, on_delete=models.CASCADE, related_name='posts_of_community', null=True, blank=True)
    is_published = models.BooleanField()

    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('post',kwargs={'slug':self.slug})
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        rstring = generate_random_string(8)
        if len(str(self.title).split()) <= 7:
            self.slug = slugify(str(self.title) + f'_{rstring}')
        self.slug = slugify(' '.join(((str(self.title)).split())[:10])+f'_{rstring}')
        super().save(*args, **kwargs)


