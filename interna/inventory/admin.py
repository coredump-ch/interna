from django.contrib import admin

from . import models


class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'identifier', 'owner', 'since')
    list_filter = ('category', 'owner', 'manager')
    save_as = True


admin.site.register(models.Item, ItemAdmin)
