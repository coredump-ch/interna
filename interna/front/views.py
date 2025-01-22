from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic.base import View, TemplateView

from memberdb import models


class HomeView(TemplateView):
    template_name = 'front/home.html'


class LogoutView(View):
    """Log the user out, redirect to home view, show a message."""

    def get(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'You have successfully logged out.')
        return redirect('front:home')


class MembersView(LoginRequiredMixin, TemplateView):
    """List members."""
    template_name = 'front/members.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        active_members = [m.Member for m in models.Membership.active.all()]
        context['active_memberships'] = models.Membership.active.order_by('Member__id')
        context['expired_members'] = set([
            m.Member for m in models.Membership.expired.order_by('start', 'Member__id')
            if m.Member not in active_members
        ])
        return context


class MemberEmailsView(LoginRequiredMixin, TemplateView):
    """List email addresses of all active members."""
    template_name = 'front/member_emails.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['memberships'] = models.Membership.active.all()
        return context
