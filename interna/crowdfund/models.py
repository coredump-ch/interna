from datetime import date

from django.conf import settings
from django.db import models
from django.db.models import Q

from sorl.thumbnail import ImageField


class Project(models.Model):
    title = models.CharField(max_length=80,
            help_text='What do you want to fund?')
    initiator = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    short_description = models.CharField(max_length=300,
            help_text='Describe your project in 300 characters or less')
    long_description = models.TextField(
            help_text='Describe your project in more detail')
    image = ImageField(upload_to='crowdfund_projects/',
            help_text='A photo showing your project')
    amount_required = models.PositiveIntegerField(
            help_text='How many CHF does this project need to be funded?')
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

    def promises(self):
        condition = Q(expiry_date__isnull=True) | Q(expiry_date__gte=date.today())
        return self.fundingpromise_set.filter(condition).order_by('-amount')

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
