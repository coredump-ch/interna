from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from . import models, forms


class IndexView(ListView):
    model = models.Project
    template_name = 'crowdfund/list.html'


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
