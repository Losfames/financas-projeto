from urllib import request
from django.shortcuts import render, redirect
from .models import Usuario
from django.shortcuts import render, redirect
from .models import Projeto
from datetime import datetime
from .models import Despesa, TipoDespesa, Projeto, Categoria
from django.db.models import Sum

categorias = Categoria.objects.all()


def home(request):
    if request.session.get('usuario_id'):
        return redirect('dashboard')  # já logado
    else:
        return redirect('login')  # não logado

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

        try:
            data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d')
            data_fim = datetime.strptime(data_fim, '%Y-%m-%d')
        except:
            return render(request, 'criar_projeto.html', {
                'erro': 'Data inválida'
            })

        if data_fim < data_inicio:
            return render(request, 'criar_projeto.html', {
                'erro': 'A data final não pode ser menor que a inicial'
            })

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
        return redirect('dashboard')  # 👈 aqui não dá pra usar projeto.id

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
                'erro': 'Data inválida'
            })

        if data_fim < data_inicio:
            return render(request, 'editar_projeto.html', {
                'projeto': projeto,
                'erro': 'A data final é menor que a inicial'
            })

        projeto.data_inicio = data_inicio
        projeto.data_fim = data_fim

        projeto.save()
        return redirect('ver_projeto', projeto_id=projeto.id)

    return render(request, 'editar_projeto.html', {'projeto': projeto})

    return render(request, 'editar_projeto.html', {'projeto': projeto})

def deletar_projeto(request, id):
    user_id = request.session.get('usuario_id')

    projeto = Projeto.objects.filter(id=id, usuario_id=user_id).first()

    if projeto:
        projeto.delete()

    return redirect('dashboard')



def ver_projeto(request, projeto_id):
    user_id = request.session.get('usuario_id')

    projeto = Projeto.objects.filter(id=projeto_id, usuario_id=user_id).first()

    if not projeto:
        return redirect('dashboard')

    despesas = Despesa.objects.filter(projeto=projeto)

    total_orcado = despesas.aggregate(Sum('valor_orcado'))['valor_orcado__sum'] or 0
    total_realizado = despesas.aggregate(Sum('valor_realizado'))['valor_realizado__sum'] or 0


    categorias = []
    valores = []

    dados = despesas.values('tipo__nome').annotate(
        total=Sum('valor_realizado')
    )

    for item in dados:
        categorias.append(item['tipo__nome'])
        valores.append(float(item['total']))

    return render(request, 'ver_projeto.html', {
        'projeto': projeto,
        'despesas': despesas,
        'total_orcado': total_orcado,
        'total_realizado': total_realizado,
        'categorias': categorias,
        'valores': valores
    })



def criar_despesa(request, projeto_id):
    user_id = request.session.get('usuario_id')

    projeto = Projeto.objects.filter(id=projeto_id, usuario_id=user_id).first()

    if not projeto:
        return redirect('dashboard')

    tipos = TipoDespesa.objects.all()

    if request.method == 'POST':
        descricao = request.POST.get('descricao')
        valor_orcado = request.POST.get('valor_orcado')
        valor_realizado = request.POST.get('valor_realizado')
        data = request.POST.get('data')

        tipo_nome = request.POST.get('tipo_nome')
        tipo_id = request.POST.get('tipo')

        if tipo_nome:
            tipo, _ = TipoDespesa.objects.get_or_create(nome=tipo_nome)
        else:
            tipo = TipoDespesa.objects.filter(id=tipo_id).first()

        if not tipo:
            return render(request, 'criar_despesa.html', {
                'erro': 'Tipo inválido',
                'tipos': tipos,
                'projeto': projeto
            })

        Despesa.objects.create(
            descricao=descricao,
            valor_orcado=valor_orcado,
            valor_realizado=valor_realizado,
            data=data,
            tipo=tipo,
            projeto=projeto
        )

        return redirect('ver_projeto', projeto_id=projeto.id)

    return render(request, 'criar_despesa.html', {
        'projeto': projeto,
        'tipos': tipos
    })



def deletar_despesa(request, id):
    user_id = request.session.get('usuario_id')

    despesa = Despesa.objects.filter(id=id, projeto__usuario_id=user_id).first()

    if not despesa:
        return redirect('dashboard')

    projeto_id = despesa.projeto.id
    despesa.delete()

    return redirect('ver_projeto', projeto_id=projeto_id)