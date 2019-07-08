import io
from zipfile import ZipFile, ZIP_DEFLATED

from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.generic.detail import BaseDetailView, DetailView
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


class Label(BaseDetailView):
    model = models.Item

    def get(self, request, *args, **kwargs):
        # Get model instance
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)

        # The brother file format needs to know the length of the string.
        # Newlines are counted as 1.
        context['charlen'] = len(self.object.name) \
            + 1 + len(self.object.owner) \
            + 1 + len(self.object.identifier)

        # Render templates
        label = render_to_string('ptouch/label.xml', context=context).replace('\n', '\r\n')
        prop = render_to_string('ptouch/prop.xml', context=context).replace('\n', '\r\n')

        # Create ZIP archive
        zipbytes = io.BytesIO()
        archive = ZipFile(zipbytes, mode='w', compression=ZIP_DEFLATED)
        archive.writestr('label.xml', label)
        archive.writestr('prop.xml', prop)
        archive.close()

        # Return response
        response = HttpResponse(zipbytes.getvalue(), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="{}.lbx"'.format(
            self.object.identifier,
        )
        return response
