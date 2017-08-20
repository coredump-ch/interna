from django.contrib import admin

from sorl.thumbnail.admin import AdminImageMixin

from . import models


class ProjectAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ('title', 'amount_required', 'created')


admin.site.register(models.Project, ProjectAdmin)
