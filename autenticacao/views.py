from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout

from autenticacao.forms import RegistrarForm, LoginForm


def registrar(request):
    if request.method == 'POST':
        form = RegistrarForm(request.POST)
        if form.is_valid():
            _, apto_para_agendamento = form.save()

            if apto_para_agendamento:
                messages.success(request, "Cadastro realizado com sucesso! Você está apto para agendamento.")
            else:
                messages.info(request, "Cadastro realizado com sucesso, porém, você não está apto para agendamento.")

            return redirect('autenticacao:login')
        else:
            return render(request, 'autenticacao/registro.html', {'form': form})

    else:
        form = RegistrarForm()

    return render(request, 'autenticacao/registro.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None and user.is_active:
                django_login(request, user)
                messages.success(request, "Login realizado com sucesso!")
                return redirect('base:home')
            else:
                messages.error(request, "Conta de usuário não está ativa.")
        else:
            return render(request, 'autenticacao/login.html', {'form': form})
    else:
        form = LoginForm()

    return render(request, 'autenticacao/login.html', {'form': form})


@login_required
def logout(request):
    django_logout(request)
    return redirect('autenticacao:login')
