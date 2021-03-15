from django.forms import ModelForm

from crispy_forms.bootstrap import FormActions, AppendedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit

from . import models


class FundingPromiseForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.html5_required = True
        self.helper.layout = Layout(
            Field('project', type='hidden'),
            'name',
            'email',
            AppendedText('amount', 'CHF'),
            AppendedText(
                'expiry_date',
                '<span class="glyphicon glyphicon-calendar"></span>',
                template='crowdfund/datepickerfield.html',
            ),
            FormActions(
                Submit('submit', 'Angebot übermitteln')
            )
        )

    class Meta:
        model = models.FundingPromise
        fields = ('project', 'name', 'email', 'amount', 'expiry_date')
