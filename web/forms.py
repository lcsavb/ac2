from django import forms
from django.db import transaction
from .models import Patient
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Row, Column, Submit
from users.models import Issuer


class CreatePatient(forms.ModelForm):
    issuers = forms.ModelChoiceField(queryset=Issuer.objects.none())  # Empty queryset as default
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(CreatePatient, self).__init__(*args, **kwargs)
        self.fields['issuers'].queryset = self.user.issuer.all()
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

    class Meta:
        labels = {
            'name': 'Nome',
            'age': 'Idade',
            'gender': 'Gênero',
            'mother_name': 'Nome da mãe',
            'disabled': 'Deficiente',
            'responsible': 'Responsável',
            'identity': 'Identidade',
            'weight': 'Peso',
            'height': 'Altura',
            'ethnicity': 'Etnia',
            'social_security_number': 'Número do seguro social',
            'sus_number': 'Número do SUS',
            'email': 'E-mail',
            'city': 'Cidade',
            'address': 'Endereço',
            'zip_code': 'CEP',
            'telephone': 'Telefone',
            'telephone_2': 'Telefone 2',
        }

        model = Patient

        fields = ['name', 
                  'age', 
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
                  'telephone_2']

        localized_fields = '__all__'

        @transaction.atomic
        def save(self, commit=True):
            print("save called with commit =", commit)
            patient = super().save(commit=False)
            if commit:
                patient.save()
                issuer = self.cleaned_data.get('issuers')
                user = self.user
                print("creating PatientCareLink with issuer =", issuer, "and user =", user)
            return patient
