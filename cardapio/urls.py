"""Rotas da aplicacao Cardapio."""

from django.urls import path

from . import views

urlpatterns = [
    # Fluxos do cliente
    path('', views.menu_cardapio, name='menu_cardapio'),
    path('carrinho/', views.carrinho_detalhe, name='carrinho_detalhe'),
    path('produto/<int:produto_id>/adicionar/', views.adicionar_ao_carrinho, name='adicionar_ao_carrinho'),
    path('carrinho/item/<int:produto_id>/atualizar/', views.atualizar_carrinho, name='atualizar_carrinho'),
    path('checkout/', views.finalizar_pedido, name='finalizar_pedido'),

    # Fluxos de administracao
    path('painel/login/', views.login_admin, name='admin_login'),
    path('painel/logout/', views.logout_admin, name='admin_logout'),
    path('painel/', views.admin_painel, name='admin_painel'),

    # CRUD Produtos
    path('painel/produtos/', views.produto_listar, name='produto_listar'),
    path('painel/produtos/novo/', views.produto_criar, name='produto_criar'),
    path('painel/produtos/editar/<int:produto_id>/', views.produto_editar, name='produto_editar'),
    path('painel/produtos/remover/<int:produto_id>/', views.produto_remover, name='produto_remover'),

    # Historico e relatorios
    path('painel/pedidos/historico/', views.historico_pedidos, name='historico_pedidos'),
    path('painel/pedidos/relatorio/', views.relatorio_vendas, name='relatorio_vendas'),
]
