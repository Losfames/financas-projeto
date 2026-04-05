from django.shortcuts import render, redirect
from .models import Usuario

# CADASTRO
def cadastro(request):
    if request.method == 'POST':
        Usuario.objects.create(
            nome=request.POST.get('nome'),
            email=request.POST.get('email'),
            senha=request.POST.get('senha'),
            cpf=request.POST.get('cpf')
        )
        return redirect('login')

    return render(request, 'cadastro.html')


# LOGIN
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        usuario = Usuario.objects.filter(email=email).first()

        if usuario and usuario.senha == senha:
            return render(request, 'home.html', {'usuario': usuario})
        else:
            return render(request, 'login.html', {'erro': 'Email ou senha inválidos'})

    return render(request, 'login.html')