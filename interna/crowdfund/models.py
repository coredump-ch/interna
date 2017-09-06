from datetime import date

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.urls import reverse

from sorl.thumbnail import ImageField


class Project(models.Model):
    title = models.CharField('Titel', max_length=80,
            help_text='Titel deines Projektes')
    initiator = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    short_description = models.CharField('Kurzbeschreibung', max_length=300,
            help_text='Beschreibe dein Projekt mit weniger als 300 Buchstaben')
    long_description = models.TextField('Detailbeschreibung',
            help_text='Beschreibe dein Projekt im Detail')
    image = ImageField('Bild', upload_to='crowdfund_projects/',
            help_text='Ein Bild, welches das Projekt repräsentiert')
    amount_required = models.PositiveIntegerField('Betrag',
            help_text='Wie viele CHF werden benötigt, um das Projekt zu finanzieren?')
    created = models.DateTimeField(auto_now_add=True, editable=False,
            help_text='When was this funding project launched?')

    def amount_funded(self):
        total = 0
        condition = Q(expiry_date__isnull=True) | Q(expiry_date__gte=date.today())
        for promise in self.fundingpromise_set.filter(condition):
            total += promise.amount
        return total

    def percent_funded(self):
        return int(self.amount_funded() / self.amount_required * 100)

    def active_promises(self):
        condition = Q(expiry_date__isnull=True) | Q(expiry_date__gte=date.today())
        return self.fundingpromise_set \
                .filter(condition) \
                .order_by('-amount')

    def expired_promises(self):
        return self.fundingpromise_set \
                .filter(expiry_date__lt=date.today()) \
                .order_by('-amount')

    def all_promises(self):
        return self.fundingpromise_set \
                .all() \
                .order_by('-amount')

    def get_absolute_url(self):
        return reverse('crowdfund:detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ('-created', 'title')

    def __str__(self):
        return self.title


class FundingPromise(models.Model):
    """
    A user promises to help funding a project with a ceratain amount.
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField('Name', max_length=100,
            help_text='Dein Name')
    amount = models.PositiveIntegerField('Betrag',
            help_text='Wie viel würdest du für dieses Projekt bezahlen?')
    created = models.DateTimeField(auto_now_add=True, editable=False,
            help_text='Wann wurde dieses Angebot hinzugefügt?')
    expiry_date = models.DateField('Ablaufdatum', blank=True, null=True,
            help_text='Soll das Angebot irgendwann ablaufen? Lasse dieses Feld leer, wenn das Angebot nie enden soll.')

    class Meta:
        ordering = ('-created',)

    def is_expired(self) -> bool:
        return self.expiry_date and (date.today() > self.expiry_date)
