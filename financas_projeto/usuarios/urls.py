from django.urls import path
from . import views


urlpatterns = [
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('criar-projeto/', views.criar_projeto, name='criar_projeto'),
    path('editar-projeto/<int:id>/', views.editar_projeto, name='editar_projeto'),
]