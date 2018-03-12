from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from . import models, forms


class Index(ListView):
    model = models.Project
    template_name = 'crowdfund/list.html'


class Detail(DetailView):
    model = models.Project
    template_name = 'crowdfund/detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['fund_form'] = forms.FundingPromiseForm(initial={
            'project': self.object.pk,
        })
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        form = forms.FundingPromiseForm(request.POST)
        if not form.is_valid():
            return HttpResponse('Invalid form submission')
        if form.cleaned_data.get('project') != self.object:
            raise ValueError('Funding project does not match current project page')
        form.save()

        msg = 'Dein Beitrag wurde gespeichert, vielen Dank!'
        messages.add_message(request, messages.INFO, msg)
        response = HttpResponseRedirect(reverse('crowdfund:detail', kwargs={'pk': self.object.pk}))
        response.set_cookie('last_pledge_name', form.cleaned_data.get('name'),
                max_age=3600 * 24 * 365)
        return response


class Create(LoginRequiredMixin, CreateView):
    model = models.Project
    fields = ['title', 'short_description', 'long_description', 'image',
              'amount_required', 'forum_thread']
    template_name = 'crowdfund/create.html'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()
        form.helper.add_input(Submit('submit', 'Speichern', css_class='btn-primary'))
        return form

    def form_valid(self, form):
        # Save data
        self.object = form.save(commit=False)
        self.object.initiator = self.request.user
        self.object.save()

        # Add message
        msg = 'Dein Projekt wurde erstellt! Trage dich doch gleich als erste/n Funder ein :)'
        messages.add_message(self.request, messages.INFO, msg)

        return HttpResponseRedirect(self.get_success_url())


class Edit(LoginRequiredMixin, UpdateView):
    model = models.Project
    fields = ['title', 'short_description', 'long_description', 'image',
              'amount_required', 'forum_thread']
    template_name = 'crowdfund/edit.html'

    def get(self, request, *args, **kwargs):
        # Ensure permission
        self.object = self.get_object()
        if self.object.initiator != request.user:
            return HttpResponse('Forbidden: Not your project', status=403)
        if self.object.funded is not None:
            return HttpResponse('Forbidden: Funded project', status=403)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # Ensure permission
        self.object = self.get_object()
        if self.object.initiator != request.user:
            return HttpResponse('Forbidden: Not your project', status=403)
        if self.object.funded is not None:
            return HttpResponse('Forbidden: Funded project', status=403)
        return super().post(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()
        form.helper.add_input(Submit('submit', 'Änderungen speichern', css_class='btn-primary'))
        return form
