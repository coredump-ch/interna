from __future__ import print_function, division, absolute_import, unicode_literals

from django.contrib import admin

from . import models


class MemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'city', 'twitter', 'github')
    search_fields = ('name', 'pk', 'emai', 'phone', 'city', 'twitter', 'github')
    list_filter = ('city',)


class MembershipAdmin(admin.ModelAdmin):
    list_display = ('Member', 'start', 'end', 'category')
    list_filter = ('Member', 'category')


class MemberPaymentAdmin(admin.ModelAdmin):
    list_display = ('Membership', 'year', 'amount')
    list_filter = ('Membership__Member', 'year')


admin.site.register(models.Member, MemberAdmin)
admin.site.register(models.Membership, MembershipAdmin)
admin.site.register(models.MemberPayment, MemberPaymentAdmin)
