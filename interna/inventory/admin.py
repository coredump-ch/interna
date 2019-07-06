from django.contrib import admin

from . import models


class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'identifier', 'owner', 'since')
    list_filter = ('category', 'owner', 'manager')
    save_as = True

    def get_readonly_fields(self, request, obj=None):
        if obj:
            # Don't allow changing identifier
            return ('identifier',)
        else:
            return ()


admin.site.register(models.Item, ItemAdmin)
