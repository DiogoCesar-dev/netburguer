# cardapio/templatetags/custom_filters.py

from django import template

register = template.Library()

@register.filter
def sub(value, arg):
    """
    Filtro customizado para subtração: Retorna 'value' - 'arg'.
    Usado para calcular quantos itens faltam para o combo.
    """
    try:
        # Tenta converter os valores para inteiros e subtrair
        return int(value) - int(arg)
    except (ValueError, TypeError):
        # Retorna o valor original em caso de erro (para não quebrar)
        return value