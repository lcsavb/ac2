from typing import Any
from django import forms
from django.db import transaction
from .models import Patient
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Row, Column, Submit
from django.utils.translation import gettext_lazy as _

class CreatePatient(forms.ModelForm):
   
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
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
                'gender', 'mother_name', 'disabled',
                'responsible', 'identity', 'weight',
                'height', 'ethnicity', 'social_security_number',
                'sus_number', 'email', 'city', 'address',
                'zip_code', 'telephone', 'telephone_2', 'issuer',
                Submit('submit', 'Save Patient')
            )
        )

    @transaction.atomic
    def save(self, commit=True):
        patient = super().save(commit=False)
        issuer_list = self.cleaned_data.get('issuer')
        if commit:
            patient.save()
            # The patient must be to the logged-in user and in its issuer list
            self.user.patients.add(patient)
            [patient.issuer.add(issuer) for issuer in issuer_list]
        return patient

    class Meta:
        labels = {
            'name': 'Nome', 'age': 'Idade', 'gender': 'Gênero',
            'mother_name': 'Nome da mãe', 'disabled': 'Deficiente',
            'responsible': 'Responsável', 'identity': 'Identidade',
            'weight': 'Peso', 'height': 'Altura',
            'ethnicity': 'Etnia', 'social_security_number': 'Número do seguro social',
            'sus_number': 'Número do SUS', 'email': 'E-mail',
            'city': 'Cidade',  'address': 'Endereço', 'zip_code': 'CEP',
            'telephone': 'Telefone', 'telephone_2': 'Telefone 2',
            'issuer': 'Emissor'
        }

        model = Patient

        fields = ['name', 'age', 'gender', 'mother_name', 
                  'disabled', 'responsible', 'identity', 
                  'weight', 'height', 'ethnicity',
                  'social_security_number', 'sus_number', 
                  'email', 'city', 'address', 'zip_code', 
                  'telephone',  'telephone_2', 'issuer']

        localized_fields = '__all__'


