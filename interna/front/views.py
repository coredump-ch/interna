# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.generic.base import View, TemplateView
from django.views.generic.list import ListView

from front.mixins import LoginRequiredMixin
from memberdb import models


class HomeView(TemplateView):
    template_name = 'front/home.html'


class LogoutView(View):
    """Log the user out, redirect to home view, show a message."""

    def get(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'You have successfully logged out.')
        return redirect('home')


class MembersView(LoginRequiredMixin, TemplateView):
    """List members."""
    template_name = 'front/members.html'

    def get_context_data(self, **kwargs):
        context = super(MembersView, self).get_context_data(**kwargs)
        context['active_memberships'] = models.Membership.active.order_by('start', 'Member__id')
        active_members = [m.Member for m in context['active_memberships']]
        context['expired_memberships'] = [
            m for m in models.Membership.expired.order_by('start', 'Member__id')
            if m.Member not in active_members
        ]
        return context


class CouponsView(LoginRequiredMixin, TemplateView):
    """List coupon codes."""
    template_name = 'front/coupons.html'
