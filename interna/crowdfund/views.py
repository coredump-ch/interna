from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from . import models


class IndexView(ListView):
    model = models.Project
    template_name = 'crowdfund/list.html'


class DetailView(DetailView):
    model = models.Project
    template_name = 'crowdfund/detail.html'
