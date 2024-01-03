from django.urls import path

from autenticacao.views import registrar, logout, login

app_name = 'autenticacao'

urlpatterns = [
    path('registrar/', registrar, name='registrar'),
    path('login/', login, name='login'),
    path('logout', logout, name='logout')
]