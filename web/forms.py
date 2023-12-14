from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import Patient
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Row, Column, Field, Submit

class CreatePatient(forms.ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CreatePatient, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Enter patient details here',
                Row(
                    Column('name', css_class='form-group col-md-6 mb-0'),
                    Column('age', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'
                ),
                'gender',
                'mother_name',
                'disabled',
                'responsible',
                'identity',
                'weight',
                'height',
                'ethnicity',
                'social_security_number',
                'sus_number',
                'email',
                'city',
                'address',
                'zip_code',
                'telephone',
                'telephone_2',
                Submit('submit', 'Save Patient')
            )
        )