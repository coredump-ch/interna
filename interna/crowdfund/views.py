from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from . import models, forms


class IndexView(ListView):
    model = models.Project
    template_name = 'crowdfund/list.html'


class CreateView(LoginRequiredMixin, CreateView):
    model = models.Project
    fields = ['title', 'short_description', 'long_description', 'image', 'amount_required']
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


class DetailView(DetailView):
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
        return HttpResponseRedirect(reverse('crowdfund:detail', kwargs={'pk': self.object.pk}))
