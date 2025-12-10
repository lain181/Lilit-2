from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import redirect
from treebeard.mp_tree import MP_Node

from lilit import settings
from posts.models import Posts



class Comments(MP_Node):

    comment_text = models.TextField(max_length=2048)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='comments_of_post', blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments_of_user',  blank=True)

    time_create = models.DateTimeField(auto_now_add=True)


    def get_absolute_url(self):
        return redirect('reply', kwargs={'id':self.id})
    def __str__(self):
        return self.comment_text




class Likes(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes_of_user')
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='likes_of_post', null=True)
    comment = models.ForeignKey('Comments', on_delete=models.CASCADE, related_name='likes_of_comment', null=True)
