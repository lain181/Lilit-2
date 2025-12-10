from django.db.models import Prefetch
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, DetailView

from comments.models import Comments
from comments.views import get_tree_from_flat
from posts.form import AddCommentForm
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
        form = AddCommentForm()
        post = get_object_or_404(Posts.objects.select_related('author', 'community').only('title', 'slug', 'content',
                                                                                          'author__username',
                                                                                          'community__name'
                                                                                          ).prefetch_related(
            Prefetch('theme', queryset=Themes.objects.only('theme'))),
             slug=slug)
        comments_flat = Comments.objects.filter(post=post).select_related('author').order_by('path')
        comments_tree = get_tree_from_flat(comments_flat)
        return render(request, 'posts/post.html', context={'post':post, 'form':form, 'comments':comments_tree })

    def post(self, request, slug):
        post = get_object_or_404(Posts.objects.select_related('author', 'community').only('title', 'slug', 'content',
                                                                                          'author__username',
                                                                                          'community__name'
                                                                                          ).prefetch_related(
            Prefetch('theme', queryset=Themes.objects.only('theme'))),
            slug=slug)
        comments_flat = Comments.objects.filter(post=post).select_related('author').order_by('path')
        comments_tree = get_tree_from_flat(comments_flat)

        form = AddCommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.author=request.user
            comment.post=post
            comment = Comments.add_root(instance=comment)

            return redirect('post', slug = slug)

        return render(request, 'posts/post.html', context={'post': post, 'form': form, 'comments': comments_tree})



class CreatePost(CreateView):
    model = Posts
    template_name = 'posts/create_post.html'
    fields = ["title", "content", "theme", "is_published"]

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return reverse_lazy('feed')
    def form_valid(self, form):
        post = form.save(commit = False)
        post.author = self.request.user
        post.save()
        return super().form_valid(form)


class PostsByTheme(ListView):

    paginate_by = 10
    model = Posts
    template_name = 'posts/posts_by_theme.html'
    context_object_name = 'posts_by_theme'

    def get_queryset(self):
        self.theme = get_object_or_404(Themes, slug = self.kwargs['slug'])
        return Posts.objects.filter(theme = self.theme, is_published = True).select_related(
           'author' , 'community').only("title", "slug", "content", "author__username", "community__name"
                                        ).prefetch_related(Prefetch('theme', queryset=  Themes.objects.only('theme'))).order_by('-time_create')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['theme'] = self.theme
        return context











