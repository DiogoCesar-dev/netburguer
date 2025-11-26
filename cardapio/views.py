"""Views principais do sistema NetBurguer."""

from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import json
from urllib.parse import quote

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.http import HttpResponseServerError
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .models import Pedido, Produto


def _converter_preco(valor):
    """Converte o valor recebido do formulario para Decimal."""
    if valor in (None, ''):
        return None
    try:
        decimal_valor = Decimal(str(valor).replace(',', '.'))
    except (InvalidOperation, TypeError, AttributeError):
        return None
    if decimal_valor < 0:
        return None
    try:
        return decimal_valor.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    except InvalidOperation:
        return None


class Carrinho:
    """Representa o carrinho de compras armazenado na sessao."""

    DESCONTO_PERCENTUAL = Decimal('0.10')
    QTD_MINIMA_COMBO = 3
    CHAVE_SESSAO = 'carrinho'

    def __init__(self, request):
        self.session = request.session
        self.carrinho = self.session.get(self.CHAVE_SESSAO, {})

    def salvar(self):
        """Persiste o carrinho na sessao do usuario."""
        self.session[self.CHAVE_SESSAO] = self.carrinho
        self.session.modified = True

    def adicionar(self, produto, quantidade=1):
        """Adiciona um produto ao carrinho."""
        try:
            quantidade = int(quantidade)
        except (TypeError, ValueError):
            quantidade = 1

        quantidade = max(1, quantidade)
        produto_id = str(produto.id)

        if produto_id not in self.carrinho:
            self.carrinho[produto_id] = {
                'id': produto.id,
                'nome': produto.nome,
                'preco': str(produto.preco),
                'quantidade': 0,
            }

        self.carrinho[produto_id]['quantidade'] += quantidade
        self.salvar()

    def atualizar(self, produto_id, nova_qtd):
        """Atualiza a quantidade de um item ou remove quando zero."""
        produto_id = str(produto_id)
        try:
            nova_qtd = int(nova_qtd)
        except (TypeError, ValueError):
            return

        if produto_id not in self.carrinho:
            return

        if nova_qtd > 0:
            self.carrinho[produto_id]['quantidade'] = nova_qtd
        else:
            self.remover(produto_id)

        self.salvar()

    def remover(self, produto_id):
        """Remove um item do carrinho."""
        produto_id = str(produto_id)
        if produto_id in self.carrinho:
            del self.carrinho[produto_id]
            self.salvar()

    def itens_distintos(self):
        """Retorna quantos produtos diferentes estao no carrinho."""
        return len(self.carrinho)

    def faltam_para_combo(self):
        """Calcula quantos itens ainda faltam para liberar o desconto."""
        return max(0, self.QTD_MINIMA_COMBO - self.itens_distintos())

    def verificar_desconto_combo(self):
        """Verifica se o combo promocional pode ser aplicado."""
        return self.itens_distintos() >= self.QTD_MINIMA_COMBO

    def calcular_total_bruto(self):
        """Calcula o total antes dos descontos."""
        total = Decimal('0.00')
        for item in self.carrinho.values():
            total += Decimal(item['preco']) * item['quantidade']
        return total

    def calcular_total_final(self):
        """Retorna o total com desconto aplicado e o valor abatido."""
        total_bruto = self.calcular_total_bruto()
        desconto = Decimal('0.00')

        if self.verificar_desconto_combo():
            desconto = total_bruto * self.DESCONTO_PERCENTUAL

        total_final = total_bruto - desconto
        return total_final, desconto

    def validar_itens(self):
        """Garante que o carrinho possui itens validos."""
        return not self.esta_vazio() and all(
            item['quantidade'] > 0 for item in self.carrinho.values()
        )

    def esta_vazio(self):
        return self.itens_distintos() == 0

    def limpar_carrinho(self):
        """Remove o carrinho da sessao."""
        if self.CHAVE_SESSAO in self.session:
            del self.session[self.CHAVE_SESSAO]
            self.session.modified = True
        self.carrinho = {}

    def serializar_itens(self, itens=None):
        """Converte o carrinho para uma lista pronta para persistencia."""
        itens_convertidos = itens if itens is not None else list(self)
        resultado = []
        for item in itens_convertidos:
            resultado.append(
                {
                    'produto_id': item['id'],
                    'nome': item['nome'],
                    'quantidade': item['quantidade'],
                    'preco': f"{item['preco']:.2f}",
                    'total': f"{item['total']:.2f}",
                }
            )
        return resultado

    def __iter__(self):
        """Permite iterar pelos itens para uso nos templates."""
        for item in self.carrinho.values():
            preco = Decimal(item['preco'])
            quantidade = item['quantidade']
            yield {
                'id': item['id'],
                'nome': item['nome'],
                'preco': preco,
                'quantidade': quantidade,
                'total': preco * quantidade,
            }

    def __len__(self):
        return sum(item['quantidade'] for item in self.carrinho.values())


# ---------------------------
# Autenticacao e Administracao
# ---------------------------


def login_admin(request):
    """Realiza o login do administrador."""
    if request.user.is_authenticated:
        return redirect('admin_painel')

    if request.method == 'POST':
        username = request.POST.get('username')
        senha = request.POST.get('password')
        user = authenticate(request, username=username, password=senha)

        if user is not None:
            login(request, user)
            return redirect('admin_painel')

        messages.error(request, 'Credenciais invalidas. Tente novamente.')

    return render(request, 'admin/login.html')


@login_required
def logout_admin(request):
    logout(request)
    return redirect('menu_cardapio')


@login_required
def admin_painel(request):
    return render(request, 'admin/painel.html')


@login_required
def produto_listar(request):
    produtos = Produto.objects.all()
    return render(request, 'admin/produto_lista.html', {'produtos': produtos})


@login_required
def produto_criar(request):
    if request.method == 'POST':
        preco = _converter_preco(request.POST.get('preco'))
        if preco is None:
            messages.error(request, 'Informe um preco valido.')
            return render(request, 'admin/produto_form.html', {'acao': 'Criar'})

        Produto.objects.create(
            nome=request.POST.get('nome'),
            descricao=request.POST.get('descricao'),
            preco=preco,
        )
        messages.success(request, 'Produto cadastrado com sucesso.')
        return redirect('produto_listar')

    return render(request, 'admin/produto_form.html', {'acao': 'Criar'})


@login_required
def produto_editar(request, produto_id):
    produto = get_object_or_404(Produto, pk=produto_id)

    if request.method == 'POST':
        preco = _converter_preco(request.POST.get('preco'))
        if preco is None:
            messages.error(request, 'Informe um preco valido.')
            return render(
                request, 'admin/produto_form.html', {'produto': produto, 'acao': 'Editar'}
            )

        produto.nome = request.POST.get('nome')
        produto.descricao = request.POST.get('descricao')
        produto.preco = preco
        produto.save()

        messages.success(request, 'Produto atualizado com sucesso.')
        return redirect('produto_listar')

    return render(request, 'admin/produto_form.html', {'produto': produto, 'acao': 'Editar'})


@login_required
def produto_remover(request, produto_id):
    produto = get_object_or_404(Produto, pk=produto_id)

    if request.method == 'POST':
        produto.delete()
        messages.success(request, 'Produto removido.')

    return redirect('produto_listar')


# ---------------------------
# Fluxos do cliente
# ---------------------------


def menu_cardapio(request):
    """Lista os produtos disponiveis."""
    try:
        produtos = Produto.objects.all()
    except Exception:
        return HttpResponseServerError(
            'Erro ao carregar cardapio. Tente novamente mais tarde.'
        )

    if not produtos.exists():
        return render(
            request,
            'cliente/menu.html',
            {
                'mensagem_erro': 'Nao ha produtos cadastrados no momento.',
                'combo_minimo': Carrinho.QTD_MINIMA_COMBO,
            },
        )

    return render(
        request,
        'cliente/menu.html',
        {'produtos': produtos, 'combo_minimo': Carrinho.QTD_MINIMA_COMBO},
    )


def adicionar_ao_carrinho(request, produto_id):
    if request.method != 'POST':
        return redirect('menu_cardapio')

    produto = get_object_or_404(Produto, id=produto_id)
    quantidade = request.POST.get('quantidade', 1)

    carrinho = Carrinho(request)
    carrinho.adicionar(produto, quantidade)
    messages.success(request, f'{produto.nome} adicionado ao carrinho.')
    return redirect('menu_cardapio')


def atualizar_carrinho(request, produto_id):
    if request.method != 'POST':
        return redirect('carrinho_detalhe')

    nova_qtd = request.POST.get('quantidade', 0)
    carrinho = Carrinho(request)
    carrinho.atualizar(produto_id, nova_qtd)
    return redirect('carrinho_detalhe')


def carrinho_detalhe(request):
    carrinho = Carrinho(request)
    total_bruto = carrinho.calcular_total_bruto()
    total_final, desconto = carrinho.calcular_total_final()

    context = {
        'carrinho': carrinho,
        'total_bruto': total_bruto,
        'desconto_aplicado': desconto,
        'total_final': total_final,
        'tem_desconto': carrinho.verificar_desconto_combo(),
        'faltam_para_combo': carrinho.faltam_para_combo(),
        'combo_minimo': Carrinho.QTD_MINIMA_COMBO,
    }
    return render(request, 'cliente/carrinho.html', context)


# ---------------------------
# Finalizacao do pedido (WhatsApp)
# ---------------------------


def _gerar_mensagem_formatada(nome, endereco, itens, total_final, desconto, total_bruto):
    linhas = [
        '*NETBURGUER - NOVO PEDIDO*',
        '',
        f'Cliente: {nome}',
        f'Entrega: {endereco}',
        '',
        '*Itens:*',
    ]

    for item in itens:
        linhas.append(f" - {item['quantidade']}x {item['nome']} (R$ {item['total']:.2f})")

    linhas.append('')

    if desconto > 0:
        linhas.append(f'Subtotal: R$ {total_bruto:.2f}')
        percentual = int(Carrinho.DESCONTO_PERCENTUAL * 100)
        linhas.append(f'Desconto combo ({percentual}%): -R$ {desconto:.2f}')

    linhas.append(f'*TOTAL: R$ {total_final:.2f}*')
    linhas.append('')
    linhas.append('Mensagem gerada automaticamente pelo NetBurguer.')
    return '\n'.join(linhas)


def _gerar_link_whatsapp(mensagem):
    numero = getattr(settings, 'WHATSAPP_NUMERO_LOJA', '')
    texto_formatado = quote(mensagem)
    return f'https://api.whatsapp.com/send?phone={numero}&text={texto_formatado}'


def finalizar_pedido(request):
    carrinho = Carrinho(request)

    if not carrinho.validar_itens():
        messages.error(request, 'Adicione itens ao carrinho antes de finalizar o pedido.')
        return redirect('carrinho_detalhe')

    total_bruto = carrinho.calcular_total_bruto()
    total_final, desconto = carrinho.calcular_total_final()
    itens_carrinho = list(carrinho)

    dados_cliente = {'nome': '', 'endereco': ''}

    if request.method == 'POST':
        dados_cliente['nome'] = request.POST.get('nome', '').strip()
        dados_cliente['endereco'] = request.POST.get('endereco', '').strip()

        if not dados_cliente['nome'] or not dados_cliente['endereco']:
            context = {
                'carrinho': carrinho,
                'total_final': total_final,
                'total_bruto': total_bruto,
                'desconto_aplicado': desconto,
                'erro': 'Preencha todos os campos obrigatorios.',
                'dados_cliente': dados_cliente,
            }
            return render(request, 'cliente/finalizar_pedido.html', context)

        mensagem = _gerar_mensagem_formatada(
            dados_cliente['nome'],
            dados_cliente['endereco'],
            itens_carrinho,
            total_final,
            desconto,
            total_bruto,
        )
        whatsapp_link = _gerar_link_whatsapp(mensagem)

        try:
            Pedido.objects.create(
                nome_cliente=dados_cliente['nome'],
                endereco_entrega=dados_cliente['endereco'],
                total_bruto=total_bruto,
                desconto_aplicado=desconto,
                total_final=total_final,
                itens_json=json.dumps(
                    carrinho.serializar_itens(itens_carrinho), ensure_ascii=False
                ),
            )
        except Exception:
            context = {
                'carrinho': carrinho,
                'total_final': total_final,
                'total_bruto': total_bruto,
                'desconto_aplicado': desconto,
                'erro': 'Erro ao salvar o pedido. Tente novamente.',
                'dados_cliente': dados_cliente,
            }
            return render(request, 'cliente/finalizar_pedido.html', context)

        carrinho.limpar_carrinho()
        return redirect(whatsapp_link)

    context = {
        'carrinho': carrinho,
        'total_final': total_final,
        'total_bruto': total_bruto,
        'desconto_aplicado': desconto,
        'dados_cliente': dados_cliente,
    }
    return render(request, 'cliente/finalizar_pedido.html', context)


# ---------------------------
# Historico e relatorios
# ---------------------------


@login_required
def historico_pedidos(request):
    filtros = {
        'data_inicio': request.GET.get('data_inicio', ''),
        'data_fim': request.GET.get('data_fim', ''),
    }

    try:
        pedidos = Pedido.objects.all().order_by('-data_criacao')

        if filtros['data_inicio']:
            pedidos = pedidos.filter(data_criacao__date__gte=filtros['data_inicio'])

        if filtros['data_fim']:
            pedidos = pedidos.filter(data_criacao__date__lte=filtros['data_fim'])

    except Exception:
        return render(
            request,
            'admin/historico.html',
            {'erro': 'Erro ao carregar historico de pedidos.', 'filtros': filtros},
        )

    context = {'pedidos': pedidos, 'filtros': filtros}

    if not pedidos.exists():
        context['mensagem_vazio'] = 'Nenhum pedido registrado no periodo selecionado.'

    return render(request, 'admin/historico.html', context)


@login_required
def relatorio_vendas(request):
    try:
        hoje = timezone.now().date()
        primeiro_dia_mes = hoje.replace(day=1)
        pedidos_mes = Pedido.objects.filter(data_criacao__date__gte=primeiro_dia_mes).order_by(
            '-data_criacao'
        )

        estatisticas = pedidos_mes.aggregate(
            qtd_pedidos=Count('id'),
            total_mensal=Sum('total_final'),
        )

        qtd_pedidos = estatisticas.get('qtd_pedidos') or 0
        total_mensal = estatisticas.get('total_mensal') or Decimal('0.00')

    except Exception:
        return render(
            request,
            'admin/relatorio.html',
            {'erro': 'Erro ao gerar relatorio de vendas.'},
        )

    context = {
        'qtd_pedidos': qtd_pedidos,
        'total_mensal': total_mensal,
        'mes_referencia': primeiro_dia_mes.strftime('%m/%Y'),
        'pedidos_detalhe': pedidos_mes,
    }
    return render(request, 'admin/relatorio.html', context)
