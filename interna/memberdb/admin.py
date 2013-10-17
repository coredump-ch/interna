from __future__ import print_function, division, absolute_import, unicode_literals

from django.contrib import admin

from . import models


class MemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'city')
    search_fields = ('name', 'pk', 'emai', 'phone', 'city')
    list_filter = ('city',)


class MembershipAdmin(admin.ModelAdmin):
    list_display = ('Member', 'start', 'end')
    list_filter = ('Member',)


admin.site.register(models.Member, MemberAdmin)
admin.site.register(models.Membership, MembershipAdmin)
