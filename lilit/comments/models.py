from django.contrib.auth.models import User
from django.db import models

from posts.models import Posts


class Comments(models.Model):
    comment_text = models.TextField(max_length=2048)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='comments_of_post')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments_of_user')
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies')

    def __str__(self):
        return self.comment_text


class Likes(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes_of_user')
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='likes_of_post', null=True)
    comment = models.ForeignKey('Comments', on_delete=models.CASCADE, related_name='likes_of_comment', null=True)
