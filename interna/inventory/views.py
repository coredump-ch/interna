from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from . import models


class Index(ListView):
    model = models.Item
    template_name = 'inventory/list.html'


class Detail(DetailView):
    model = models.Item
    template_name = 'inventory/detail.html'
