from django.db.models import Prefetch
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView

from comments.models import Comments
from posts.models import Posts, Themes


class FeedBase(ListView):
    ordering = ['-created_at']
    model = Posts
    template_name = 'posts/feed.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return Posts.objects.filter(is_published = True).select_related(
           'author' , 'community').only("title", "slug", "content", "author__username", "community__name"
                                        ).prefetch_related(Prefetch('theme', queryset=  Themes.objects.only('theme')))

class PostDetail(View):
    def get(self, request, slug):
        post = Posts.objects.filter(slug=slug).select_related('author', 'community').only('title', 'slug', 'content', 'author__username', 'community__name'
                                        ).prefetch_related(Prefetch('theme', queryset=Themes.objects.only('theme')), Prefetch('comments_of_post', queryset=Comments.objects.all()))

        return render(request, 'posts/post.html', context={'post':post, })
