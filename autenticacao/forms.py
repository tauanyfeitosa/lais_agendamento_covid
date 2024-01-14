import datetime

from django import forms
from django.contrib.auth import authenticate
from django.db import transaction
from localflavor.br.forms import BRCPFField

from autenticacao.models import UsuarioBase, Candidato, GrupoAtendimentoCandidato
from base.models import GrupoAtendimento


class RegistrarForm(forms.ModelForm):
    nome = forms.CharField(
        max_length=255,
        label='Nome Completo'
    )
    cpf = BRCPFField(
        label='CPF',
    )
    senha = forms.CharField(
            widget=forms.PasswordInput(),
            min_length=8,
            max_length=16,
            help_text='Sua senha deve ter entre 8 e 16 dígitos'
    )
    senha_confirmacao = forms.CharField(
            widget=forms.PasswordInput(),
            label='Confirmação de senha',
            min_length=8,
            max_length=16,
            help_text='Sua senha deve ter entre 8 e 16 dígitos'
    )
    data_nascimento = forms.DateField(
        label='Data de Nascimento',
        widget=forms.DateInput(attrs={
            'type': 'date',
            'max': datetime.date.today().strftime('%Y-%m-%d'),
        }
        )
    )
    grupo_atendimento = forms.ModelMultipleChoiceField(
        queryset=GrupoAtendimento.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='Grupos de Atendimento'
    )

    covid_30_dias = forms.BooleanField(
        required=False,
        label='Teve Covid nos últimos 30 dias?'
    )

    def clean_cpf(self):
        cpf = self.cleaned_data['cpf']
        cpf = cpf.replace('.', '').replace('-', '')

        if UsuarioBase.objects.filter(cpf=cpf).exists():
            self.add_error('cpf','CPF já cadastrado no sistema.')
        return cpf

    def clean_data_nascimento(self):
        data_nascimento = self.cleaned_data['data_nascimento']

        if data_nascimento > datetime.date.today():
            self.add_error('data_nascimento','Data de nascimento não pode ser maior que a data atual.')
        return data_nascimento

    def clean(self):
        senha = self.cleaned_data['senha']
        senha_confirmacao = self.cleaned_data['senha_confirmacao']

        if senha != senha_confirmacao:
            self.add_error('senha','As senhas não conferem.')

    class Meta:
        model = Candidato
        fields = ['nome','cpf', 'senha', 'senha_confirmacao', 'data_nascimento', 'grupo_atendimento', 'covid_30_dias']

    def save(self, commit=True):
        with transaction.atomic():
            cpf = self.cleaned_data['cpf']
            senha = self.cleaned_data['senha']
            nome = self.cleaned_data['nome']
            data_nascimento = self.cleaned_data['data_nascimento']
            covid_30_dias = self.cleaned_data.get('covid_30_dias', False)

            usuario_base = UsuarioBase.objects.create_user(cpf=cpf, password=senha)

            candidato = Candidato.objects.create(
                usuario_base=usuario_base,
                nome=nome,
                data_nascimento=data_nascimento,
                covid_30_dias=covid_30_dias
            )

            candidato.apto_agendamento = candidato.eh_apto_agendamento()
            candidato.save()

            if self.cleaned_data.get('grupo_atendimento'):
                for grupo in self.cleaned_data['grupo_atendimento']:
                    GrupoAtendimentoCandidato.objects.create(
                        candidato=candidato,
                        grupo_atendimento=grupo
                    )

            return candidato


class LoginForm(forms.Form):
    cpf = BRCPFField(label='CPF')
    senha = forms.CharField(widget=forms.PasswordInput(), min_length=8, max_length=12, label='Senha')

    def clean_cpf(self):
        cpf = self.cleaned_data['cpf']
        cpf = cpf.replace('.', '').replace('-', '')
        return cpf

    def clean(self):
        cleaned_data = super().clean()
        cpf = cleaned_data.get('cpf')
        senha = cleaned_data.get('senha')

        if cpf and senha:
            self.user = authenticate(username=cpf, password=senha)
            if self.user is None:
                self.add_error('cpf','CPF ou senha incorretos.')

        return cleaned_data

    def get_user(self):
        return self.user if hasattr(self, 'user') else None
