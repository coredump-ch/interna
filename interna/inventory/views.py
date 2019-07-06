from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from . import models


class Index(ListView):
    model = models.Item
    template_name = 'inventory/list.html'

    def get_queryset(self):
        category = self.request.GET.get('category')
        if category == 'none':
            return self.model.objects.filter(category__isnull=True)
        if category is not None and category in models.Item.CATEGORY:
            return self.model.objects.filter(category=category)
        return self.model.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.request.GET.get('category')
        if category is not None and category in models.Item.CATEGORY:
            count = self.model.objects.filter(category=category).count()
            context['category'] = (category, models.Item.CATEGORY[category], count)
        context['categories'] = [
            c + (self.model.objects.filter(category=c[0]).count(),)
            for c in models.Item.CATEGORY
        ]
        return context


class Detail(DetailView):
    model = models.Item
    template_name = 'inventory/detail.html'
