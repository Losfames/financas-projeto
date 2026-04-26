from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('criar-projeto/', views.criar_projeto, name='criar_projeto'),
    path('projeto/<int:projeto_id>/', views.ver_projeto, name='ver_projeto'),
    path('editar-projeto/<int:id>/', views.editar_projeto, name='editar_projeto'),
    path('deletar-projeto/<int:id>/', views.deletar_projeto, name='deletar_projeto'),
    path('projeto/<int:projeto_id>/nova-despesa/', views.criar_despesa, name='criar_despesa'),
    path('deletar-despesa/<int:id>/', views.deletar_despesa, name='deletar_despesa'),
]