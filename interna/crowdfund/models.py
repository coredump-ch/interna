from django.db import models

from sorl.thumbnail import ImageField


class Project(models.Model):
    title = models.CharField(max_length=80,
            help_text='What do you want to fund?')
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

    class Meta:
        ordering = ('-created', 'title')

    def __str__(self):
        return self.title
