from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def home(request):
    base_user = request.user
    user = base_user.candidato
    return render(request, 'home.html', locals())
