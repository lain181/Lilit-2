from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from communities.models import Communities, CommunityAdmin


class CreateCommunity(CreateView):
    model = Communities
    fields = ['name', 'about', 'themes']
    template_name = 'communities/create_community.html'

    def get_success_url(self):
        next = self.request.GET.get('next')
        if next:
            return reverse_lazy(next)
        return reverse_lazy('feed')
    def form_valid(self, form):
        community = form.save()
        CommunityAdmin.objects.create(
            community = community,
            is_creator = True,
            admin = self.request.user

        )
        return super().form_valid(form)
