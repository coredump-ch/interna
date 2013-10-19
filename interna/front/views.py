# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.generic.base import View, TemplateView


class HomeView(TemplateView):
    template_name = 'front/home.html'


class LogoutView(View):
    """Log the user out, redirect to home view, show a message."""

    def get(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'You have successfully logged out.')
        return redirect('home')
