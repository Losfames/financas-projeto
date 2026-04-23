from django.shortcuts import render, redirect
from .models import Usuario
from django.shortcuts import render, redirect
from .models import Projeto
from datetime import datetime

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
            request.session['usuario_id'] = usuario.id
            request.session['usuario_id'] = usuario.id
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'erro': 'Email ou senha inválidos'})

    return render(request, 'login.html')



def dashboard(request):
    user_id = request.session.get('usuario_id')

    if not user_id:
        return redirect('login')

    projetos = Projeto.objects.filter(usuario_id=user_id)

    return render(request, 'dashboard.html', {'projetos': projetos})



def criar_projeto(request):
    user_id = request.session.get('usuario_id')

    if request.method == 'POST':
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        data_inicio = request.POST.get('data_inicio')
        data_fim = request.POST.get('data_fim')

        Projeto.objects.create(
            nome=nome,
            descricao=descricao,
            data_inicio=data_inicio,
            data_fim=data_fim,
            usuario_id=user_id
        )

        return redirect('dashboard')

    return render(request, 'criar_projeto.html')



def editar_projeto(request, id):
    user_id = request.session.get('usuario_id')

    projeto = Projeto.objects.filter(id=id, usuario_id=user_id).first()

    if not projeto:
        return redirect('dashboard')

    if request.method == 'POST':
        projeto.nome = request.POST.get('nome')
        projeto.descricao = request.POST.get('descricao')

        data_inicio = request.POST.get('data_inicio')
        data_fim = request.POST.get('data_fim')

    try:
        data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d')
        data_fim = datetime.strptime(data_fim, '%Y-%m-%d')
    except:
        return render(request, 'editar_projeto.html', {
            'projeto': projeto,
        })

    if data_fim < data_inicio:
        return render(request, 'editar_projeto.html', {
            'projeto': projeto,
            'erro': 'A data final é menor que a inicial'
        })

    projeto.data_inicio = data_inicio
    projeto.data_fim = data_fim

    projeto.save()
    return redirect('dashboard')

    return render(request, 'editar_projeto.html', {'projeto': projeto})

