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


    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save( *args, **kwargs)


class CommunityAdmin(models.Model):
    community = models.ForeignKey(Communities, related_name='admins_of_community',on_delete=models.CASCADE )
    is_creator = models.BooleanField(default=False)
    admin = models.ForeignKey(User, related_name='user_admins', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.admin.username} is admin of {self.community.name}"

