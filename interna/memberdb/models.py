from django.db import models

from model_utils import Choices

from . import managers


class Member(models.Model):
    """A member of the association."""
    class SafeAccessType(models.TextChoices):
        APP = 'app', 'App'
        CODE = 'code', 'Code'
        NONE = 'none', 'Nein'

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=16, blank=True)
    city = models.CharField(max_length=100, blank=True,
        help_text='Wohnort')
    github = models.CharField(max_length=32, blank=True,
        help_text='Github Benutzername')
    key_number = models.CharField(max_length=100, blank=True,
        help_text='Schlüsselnummer')
    key_safe = models.CharField(max_length=100, blank=True,
        choices=SafeAccessType.choices,
        help_text='Art des Schlüsselsafe-Zugriffs')

    class Meta:
        ordering = ('name', 'id')

    def __str__(self):
        return self.name


class Membership(models.Model):
    """A membership, with a start and end date.

    This is needed as a 1:n relation because a person can leave the association
    and then re-join later on.

    """
    CATEGORY = Choices(
        (1, 'verdiener', 'Verdiener'),
        (2, 'nichtverdiener', 'Nichtverdiener'),
    )

    Member = models.ForeignKey(Member, related_name='Membership', on_delete=models.CASCADE)
    start = models.DateField()
    end = models.DateField(null=True, blank=True)
    category = models.PositiveSmallIntegerField(choices=CATEGORY)
    paid_until = models.CharField(max_length=4, blank=True)
    ccc = models.BooleanField(default=False, help_text='CCC Mitglied?')

    # Custom managers
    objects = models.Manager()
    active = managers.MembershipActivityManager(active=True)
    expired = managers.MembershipActivityManager(active=False)

    class Meta:
        ordering = ('-start', '-Member__pk')
        get_latest_by = ('end', 'start')

    def __str__(self):
        parts = []
        parts.append(self.Member.name)
        if not self.end:
            parts.append('since')
        parts.append('{}'.format(self.start))
        if self.end:
            parts.append('to {}'.format(self.end))
        return ' '.join(parts)
