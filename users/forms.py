from django.forms import ModelForm, ModelChoiceField
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from django.db import transaction
from .models import CustomUser
from users.models import Issuer, Clinic, Doctor
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Row, Column, Field, Submit

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2']

class CreateClinic(ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(CreateClinic, self).__init__(*args,**kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'create_clinic'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'POST'
        self.helper.form_action = ''
        self.helper.add_input(Submit('submit', 'Cadastrar'))
        self.helper.layout=Layout(
            Row(
                Column('name',css_class='form-group col-6 mb-0'),
                Column('sus_number',css_class='form-group col-2 mb-0'),
                Column(Field('phone',id='phone'),css_class='form-group col-4 mb-0'),
                css_class='form-row'
            ),
            Fieldset(
                'Localização',
                Row(
                    Column('city',css_class='form-group col-6 mb-0'),
                    Column('neighborhood',css_class='form-group col-6 mb-0')
                ),
                Row(
                    Column(Field('zip_code',id='zip_code'),css_class='form-group col-2 mb-0'),
                    Column('address',css_class='form-group col-8 mb-0'),
                    Column('address_number',css_class='form-group col-2 mb-0')
                )
            )
        )

    @transaction.atomic
    def save(self, commit=True):
        clinic = super().save(commit=False)
        if commit:
            clinic.save()
            self.user.clinic.add(clinic)  # Add clinic to logged-in user
        return clinic

    class Meta:
        model = Clinic
        fields = ['sus_number', 'name', 'address',
                  'address_number',  
                  'city', 'neighborhood', 'zip_code', 'phone'
        ]
        labels = {'sus_number': _('CNS'),
                  'name': _('Nome'),
                  'address_number': _('Número'),
                  'zip_code': _('CEP'),
                  'phone': _('Telefone'),
                   'city': _('Cidade'),
                   'neighborhood': _('Bairro'),
                   'address': _('Logradouro')

        }
        localized_fields = '__all__'

class CreateDoctor(ModelForm):
        clinic = ModelChoiceField(queryset=Clinic.objects.none(), required=True)

        def __init__(self, *args, **kwargs):
            self.user = kwargs.pop('user', None)
            super(CreateDoctor, self).__init__(*args,**kwargs)
            self.helper = FormHelper()
            self.helper.form_id = 'create_doctor'
            self.helper.form_class = 'blueForms'
            self.helper.form_method = 'POST'
            self.helper.form_action = ''
            self.helper.add_input(Submit('submit', 'Cadastrar'))
            self.fields['clinic'].queryset = self.user.clinic.all()
            self.fields['clinic'].label = _('A qual clínica deseja associar o médico?')
            self.helper.layout = Layout(
                Row(
                    Column('name',css_class='form-group col-6 mb-0'),
                    Column('council_number',css_class='form-group col-2 mb-0'),
                    Column('sus_number',css_class='form-group col-4 mb-0'),
                    Column('clinic',css_class='form-group col-6 mb-0'),
                    css_class='form-row'
                ),
                Fieldset(
                    'Especialidade',
                    Row(
                        Column('speciality',css_class='form-group col-6 mb-0'),
                    ),
                )
            )

        @transaction.atomic
        def save(self, commit=True):
            doctor = super().save(commit=False)
            clinic = self.cleaned_data.get('clinic')
            if commit:
                doctor.save()
                new_issuer = Issuer.objects.create(doctor=doctor, clinic=clinic)
                self.user.issuer.add(new_issuer)

            return doctor

        class Meta:
            model = Doctor
            fields = ['name', 'council_number', 'sus_number', 'speciality']
            labels = {
                'name': _('Nome completo'),
                'council_number': _('CRM'),
                'sus_number': _('Cartão Nacional de Saúde (CNS)'),
                'speciality': _('Especialidade')
            }
            localized_fields = '__all__'