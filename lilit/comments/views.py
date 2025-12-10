from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView

from comments.models import Comments


def get_tree_from_flat(comments):
    tree = []
    stack = []

    for comment in comments:
        level = comment.get_depth()-1

        while stack and stack[-1]['level']>=level:
            stack.pop()

        node = {'comment':comment, 'level':level, 'children':[]}

        if stack:
            stack[-1]['children'].append(node)

        else:
            tree.append(node)

        stack.append(node)

    def recursion_sort(node):
        node.sort(key= lambda x:(x["comment"].time_create), reverse=True)
        for el in node:
            recursion_sort(el['children'])

    recursion_sort(tree)
    return tree



class CreateReply(CreateView):
    model = Comments
    template_name = 'posts/reply.html'
    fields = ['comment_text']
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment'] = get_object_or_404(Comments, pk=self.kwargs["id"])
        return context
    def get_success_url(self):
        next_url = self.request.GET.get("next")
        if next_url:
            return next_url
        return reverse_lazy('feed')

    def form_valid(self, form):
        comment = form.save(commit = False)
        comment.author = self.request.user
        reply = get_object_or_404(Comments, pk=self.kwargs['id'])

        comment.post = reply.post
        comment = reply.add_child(instance = comment)
        return super().form_valid(form)