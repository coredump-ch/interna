from datetime import date
import logging

from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.db.models import Q, Sum
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone

from sorl.thumbnail import ImageField


logger = logging.getLogger('crowdfund.models')


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
    forum_thread = models.URLField('Forums-Thread',
            help_text='Bitte erstelle auf forum.coredump.ch in der Kategorie "Hackerspace" '
                      'einen Diskussionsthread zu diesem Crowdfunding.')
    created = models.DateTimeField(auto_now_add=True, editable=False,
            help_text='When was this funding project launched?')
    funded = models.DateTimeField(null=True, blank=True,
            help_text='When was this project funded?')

    def amount_funded(self):
        """
        Calculate the amount funded.

        This will exclude expired promises, except for promises that expired
        after the project was funded.
        """
        return self.active_promises().aggregate(total=Sum('amount'))['total'] or 0

    def percent_funded(self):
        return int(self.amount_funded() / self.amount_required * 100)

    def _get_expiry_condition(self):
        """
        Build filter expression for expired promises.

        Note: We could use the `Now` db function that gets the current date using native SQL,
        but then the function is not easily testable with mocking anymore.

        """
        condition = Q(expiry_date__isnull=True) | Q(expiry_date__gte=date.today())
        if self.funded is not None:
            condition |= Q(expiry_date__gte=self.funded)
        return condition

    def active_promises(self):
        return self.fundingpromise_set \
                .filter(self._get_expiry_condition()) \
                .order_by('-amount', 'created')

    def expired_promises(self):
        return self.fundingpromise_set \
                .exclude(self._get_expiry_condition()) \
                .order_by('-amount', 'created')

    def all_promises(self):
        return self.fundingpromise_set \
                .all() \
                .order_by('-amount', 'created')

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
            help_text='Soll das Angebot irgendwann ablaufen? Lasse dieses Feld leer, '
                      'wenn das Angebot nie enden soll.')

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '%d CHF by %s for %s' % (self.amount, self.name, self.project.title)

    def is_expired(self) -> bool:
        return self.expiry_date and (date.today() > self.expiry_date)


@receiver(post_save, sender=FundingPromise)
def on_funding_promise_save(sender, **kwargs):
    project = kwargs['instance'].project
    created = kwargs['created']
    if created is True \
            and project.funded is None \
            and project.amount_funded() >= project.amount_required:

        logger.info('Project %d (%s) is funded!' % (project.pk, project.title))

        # Update model
        project.funded = timezone.now()
        project.save(update_fields=['funded'])

        # Send e-mail to project initiator
        if project.initiator is not None:
            subject = 'Dein Projekt "%s" wurde finanziert!' % project.title
            text_content = render_to_string('emails/funding_success.txt', {'project': project})
            sender = settings.SERVER_EMAIL
            recipients = [project.initiator.email]
            send_mail(
                subject,
                text_content,
                sender,
                recipients,
                fail_silently=False
            )
