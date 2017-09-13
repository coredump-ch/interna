from django.contrib import admin

from sorl.thumbnail.admin import AdminImageMixin

from . import models


class ProjectAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ('title', 'amount_required', 'created')


class FundingPromiseAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ('project', 'name', 'amount', 'expiry_date')


admin.site.register(models.Project, ProjectAdmin)
admin.site.register(models.FundingPromise, FundingPromiseAdmin)
