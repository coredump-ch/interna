# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

from django.core.management.base import BaseCommand

from memberdb.models import Member


class Command(BaseCommand):
    help = 'Dump the access codes to stdout'

    def handle(self, *args, **options):
        values = Member.objects.values_list('email', 'access_code')
        for email, code in values:
            print('%s:%s' % (email, code))
