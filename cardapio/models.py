# cardapio/models.py
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User # Para o Administrador/CRUD

# -----------------------------------------------------
# Módulo de Produtos (CRUD Admin)
# -----------------------------------------------------
class Produto(models.Model):
    """
    Modelo Produto: Armazena os itens do cardápio.
    Métodos: objects.all(), objects.get(id) (usados na view).
    """
    nome = models.CharField(max_length=100, verbose_name="Nome do Item")
    descricao = models.TextField(verbose_name="Descrição Detalhada")
    preco = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Preço Unitário")
    is_combo = models.BooleanField(default=False, verbose_name="É um Combo?")

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        ordering = ['nome']

    def __str__(self):
        return self.nome

# -----------------------------------------------------
# Módulo de Pedidos (Histórico e Relatórios Admin)
# -----------------------------------------------------
class Pedido(models.Model):
    """
    Modelo Pedido: Armazena o registro de um pedido finalizado para histórico.
    Métodos: objects.create(), objects.filter(), objects.aggregate() (usados na view).
    """
    # Informações do Cliente (validar_campos_obrigatorios)
    nome_cliente = models.CharField(max_length=100, verbose_name="Nome do Cliente")
    endereco_entrega = models.CharField(max_length=255, verbose_name="Endereço de Entrega")
    
    # Informações Financeiras e de Rastreio
    data_criacao = models.DateTimeField(default=timezone.now, verbose_name="Data do Pedido")
    total_bruto = models.DecimalField(max_digits=8, decimal_places=2, default=0.00, verbose_name="Total Bruto")
    desconto_aplicado = models.DecimalField(max_digits=8, decimal_places=2, default=0.00, verbose_name="Desconto Aplicado")
    total_final = models.DecimalField(max_digits=8, decimal_places=2, default=0.00, verbose_name="Total Final")
    
    # Detalhe do Pedido (Serializado)
    # Armazena os itens do carrinho como JSON/Texto para persistência.
    itens_json = models.TextField(default="[]", verbose_name="Itens do Pedido (JSON)")

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ['-data_criacao']

    def __str__(self):
        return f"Pedido #{self.id} - Cliente: {self.nome_cliente} - R$ {self.total_final}"