from typing import Any
from django import forms
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from .models import Patient, Prescription
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Row, Column, Submit


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
        model = Patient        
        
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

        fields = ['name', 'age', 'gender', 'mother_name', 
                  'disabled', 'responsible', 'identity', 
                  'weight', 'height', 'ethnicity',
                  'social_security_number', 'sus_number', 
                  'email', 'city', 'address', 'zip_code', 
                  'telephone',  'telephone_2', 'issuer']

        localized_fields = '__all__'

class CreatePrescription(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(CreatePrescription, self).__init__(*args, **kwargs)

        # Dynamic fields - Each of the 4 possible drugs have 6 months of posology and qty.

        drugs = ['01', '02', '03', '04']
        months = ['01', '02', '03', '04', '05', '06']

        self.fields.update(
            {
                f'drug_{d}': forms.CharField(label=f'Medicamento {d}')
                for d in drugs
            }
        )

        self.fields.update(
            {
                f'posology_drug_{d}_month_{m}': forms.CharField(label=f'Posologia - Medicamento {d} - Mês {m}')
                for d in drugs
                for m in months
            }
        )

        self.fields.update(
            {
                f'qty_drug_{d}_month_{m}': forms.CharField(label=f'Qtde. - Medicamento {d} - Mês {m}')
                for d in drugs
                for m in months
            }
        )

    @transaction.atomic
    def save(self, commit=True):
        prescription = Prescription()
        if commit:
            prescription.save()
        return prescription


    first_time =forms.ChoiceField(initial={False}, label='Protocolo 1ª vez: ',
                                       choices=[(False, 'Não'),
                                                (True, 'Sim')],
                                                widget=forms.Select(attrs={'class':'custom-select'}))

    icd = forms.CharField(required=True, label='CID',widget=forms.TextInput(attrs={'size': 5}))
    diagnosis = forms.CharField(required=True, label='Diagnóstico',widget=forms.TextInput)
    anamnesis = forms.CharField(required=True, label='Anamnese')
    filled_by = forms.ChoiceField(initial={'paciente'},
                                       choices=[('paciente', 'Paciente'),
                                                ('mae', 'Mãe'),
                                                ('responsavel', 'Responsável'),
                                                ('medico', 'Médico')],
                                                widget=forms.Select(attrs={'class':'custom-select'}))
                                                
    previous_treatment = forms.ChoiceField(
        choices=((True, 'Sim'), (False, 'Não')),
        label='Fez tratamento prévio?',
        initial=False,
        widget=forms.Select(attrs={'class':'custom-select'})
    )
    previous_treatment_description = forms.CharField(
        label='Descrição dos tratamentos prévios',
        required=False, widget=forms.TextInput(attrs={'class':'cond-trat'})
    )
    first_date = forms.DateField(
        required=True, label='Data',
        widget=forms.DateInput(format='%d/%m/%Y'),
        input_formats=['%d/%m/%Y', ]
    )

    report = forms.CharField(
        label='Relatório',
        required=False, widget=forms.Textarea(attrs={'class':'relatorio', 'rows': '6', 'width': '100%'})
    )

    report_required = forms.ChoiceField(initial={False}, label='Emissão de relatório: ',
                                       choices=[(False, 'Não'),
                                                (True, 'Sim')],
                                                widget=forms.Select(attrs={'class':'custom-select emitir-relatorio'}))

    exams_required = forms.ChoiceField(initial={False}, label='Emissão de exames: ',
                                       choices=[(False, 'Não'),
                                                (True, 'Sim')],
                                                widget=forms.Select(attrs={'class':'custom-select'}))

    exams = forms.CharField(
        label='Exames',
        required=False, widget=forms.Textarea(attrs={'class':'exames', 'rows': '6'})
    )
