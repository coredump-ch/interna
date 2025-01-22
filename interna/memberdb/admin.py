from django.contrib import admin

from . import models


class MemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'city', 'github', 'key_number', 'key_safe')
    search_fields = ('name', 'pk', 'email', 'phone', 'city', 'github', 'key_number', 'key_safe')
    list_filter = ('city', 'key_safe')


class MembershipAdmin(admin.ModelAdmin):
    list_display = ('Member', 'start', 'end', 'category', 'paid_until', 'ccc')
    list_filter = ('Member', 'category', 'paid_until', 'ccc')


admin.site.register(models.Member, MemberAdmin)
admin.site.register(models.Membership, MembershipAdmin)
