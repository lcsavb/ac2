
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from .models import CustomUser
from users.models import Issuer
from web.models import Clinic
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Row, Column, Field, Submit

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2']

class CreateClinic(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CreateClinic, self).__init__(*args,**kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'clinica-cadastro'
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
