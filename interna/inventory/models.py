from django.core.validators import validate_slug
from django.db import models

from model_utils import Choices
from sorl.thumbnail import ImageField


class Item(models.Model):
    """
    An object in the hackerspace.
    """
    CATEGORY = Choices(
        ('manufacturing', '3D Printing, Scanning, Cutting, Plotting'),
        ('computers_network', 'Computers & Networking'),
        ('electronics_lab', 'Electronics Lab'),
        ('makerspace', 'Makerspace'),
        ('home_appliances', 'Home Appliances'),
        ('vintage', 'Vintage Computers'),
    )

    identifier = models.CharField(max_length=64, primary_key=True,
            validators=[validate_slug],
            help_text='A short lowercase identifier, e.g. "um2"')
    name = models.CharField(max_length=255,
            help_text='A short name, e.g. "Ultimaker 2+"')
    description = models.TextField(blank=True,
            help_text='Describe this item')
    image = ImageField(upload_to='inventory/', null=True, blank=True,
            help_text='A photo of this item')
    owner = models.CharField(max_length=255,
            help_text='Who owns this item? If it belongs to the hackerspace, '
                      'set this value to "Coredump".')
    manager = models.CharField(max_length=255, null=True, blank=True,
            help_text='Who should you ask if you have questions about this item?')
    category = models.CharField(max_length=255, choices=CATEGORY, null=True, blank=True,
            help_text='In what category does this device belong?')
    since = models.DateField(null=True, blank=True,
            help_text='When was this item brought to the hackerspace?')
    cost = models.IntegerField(null=True, blank=True,
            help_text='How much did this cost us (in CHF)?')
    howto_url = models.URLField(null=True, blank=True,
            help_text='An URL to a page that explains how to use this item')

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name
