NetBurguer 🍔</br>
Projeto Acadêmico — Programação Web Back-end</br>

Desenvolvido por: [Diogo Cesar Furlan da Silva] </br>
Disciplina: Programação Web Back-End</br>
Curso: Tecnologia em Sistemas para Internet</br>
Instituição: IFMT (Instituto Federal de Mato Grosso)</br>

📌 Descrição

NetBurguer é um sistema web de pedidos online desenvolvido em Django, simulando a lógica completa de um restaurante com cardápio, carrinho de compras, finalização de pedidos via WhatsApp,</br>gerenciamento administrativo, histórico e relatórios de vendas.


⚙️ Funcionalidades Implementadas</br>
📌 Para o Cliente

Visualização do cardápio</br>
Adição de itens ao carrinho</br>
Atualização de quantidades</br>
Cálculo automático de totais e descontos por combo (3 itens)</br>
Finalização do pedido</br>
Geração automática de mensagem formatada para envio via WhatsApp

📌 Para o Administrador
Login e logout</br>
Painel administrativo 

CRUD completo de produtos:</br>
Criar</br>
Editar</br>
Listar</br>
Remover

Histórico de pedidos com filtros por data</br>
Relatórios de vendas mensais com agregações</br>
Visualização detalhada dos pedidos do mês

📌 Recursos Extras

Carrinho persistido via sessão</br>
Filtros customizados em Template Tags</br>
Validações personalizadas</br>
Serialização do pedido em JSON para armazenamento definitivo

🧱 Conceitos de Programação Web Back-end Aplicados</br>
1. Arquitetura MTV

Models: Produto, Pedido</br>
Templates: Para cliente e admin, com herança e uso de filtros customizados</br>
Views: Autenticação, CRUD, Carrinho, Relatórios, Finalização via WhatsApp

2. Modelagem de Banco de Dados</br>
Entidades Principais

Produto</br>
Nome</br>
Descrição</br>
Preço</br>
Pedido</br>
Dados do cliente</br>
Totais financeiros</br>
Itens serializados em JSON</br>
Data de criação</br>
Agregações utilizadas para relatórios

3. Sistema de Autenticação

Login e logout via Django Auth</br>
Decoradores login_required protegendo rotas sensíveis</br>
Redirecionamentos definidos no settings

4. Funcionalidades Avançadas

Sessões para carrinho</br>
Método de cálculo com regras de negócio (desconto combo, total bruto, total final)</br>
Conversão e validação de valores monetários</br>
Template Tags para filtros customizados (sub)</br>
Serialização JSON segura para persistência dos itens

🧰 Tecnologias Utilizadas

Python 3.x</br>
Django 4.x</br>
SQLite</br>
HTML5 / CSS3 / JavaScript</br>
Template Engine do Django</br>
WhatsApp API para envio de pedidos</br>

📁 Estrutura do Projeto</br>
netburguer/</br>
├── cardapio/</br>
│   ├── models.py          # Modelos Produto e Pedido</br>
│   ├── views.py           # Lógica de fluxo, carrinho e administração</br>
│   ├── urls.py            # Rotas da aplicação</br>
│   ├── templatetags/</br>
│   │   └── custom_filters.py   # Filtros customizados</br>
│</br>
├── netburger/</br>
│   ├── settings.py        # Configurações principais</br>
│   ├── urls.py            # URL root</br>
│</br>
├── static/</br>
│   ├── css/style.css</br>
│   ├── img/</br>
│   └── js/</br>
│</br>
├── templates/</br>
│   ├── admin/             # Telas de administração</br>
│   │   ├── login.html</br>
│   │   ├── painel.html</br>
│   │   ├── produto_lista.html</br>
│   │   ├── produto_form.html</br>
│   │   ├── historico.html</br>
│   │   └── relatorio.html</br>
│</br>
│   ├── cliente/           # Telas para o usuário final</br>
│   │   ├── menu.html</br>
│   │   ├── carrinho.html</br>
│   │   └── finalizar_pedido.html</br>
│
├── db.sqlite3             # Banco de dados</br>
└── manage.py</br>

📦 Modelos — Código Resumido</br>
Produto</br>
class Produto(models.Model):</br>
    nome = models.CharField(max_length=100)</br>
    descricao = models.TextField()</br>
    preco = models.DecimalField(max_digits=6, decimal_places=2)</br>
    is_combo = models.BooleanField(default=False)</br>
</br>
Pedido</br>
class Pedido(models.Model):</br>
    nome_cliente = models.CharField(max_length=100)</br>
    endereco_entrega = models.CharField(max_length=255)</br>
    data_criacao = models.DateTimeField(default=timezone.now)</br>
    total_bruto = models.DecimalField(max_digits=8, decimal_places=2)</br>
    desconto_aplicado = models.DecimalField(max_digits=8, decimal_places=2)</br>
    total_final = models.DecimalField(max_digits=8, decimal_places=2)</br>
    itens_json = models.TextField(default="[]")</br>
</br>
🛒 Carrinho — Regras Implementadas</br>
</br>
Persistência via sessão</br>
Adição, remoção e atualização</br>
Desconto automático de 10% ao atingir 3 itens diferentes</br>
Serialização em JSON para armazenar no banco</br>
Iteração customizada para exibição nos templates</br>

📊 Relatórios de Venda</br>

Contagem de pedidos do mês</br>
Soma total de faturamento mensal</br>
Listagem detalhada dos pedidos</br>
Filtros por data no histórico</br>

</br>

## Instalação e execução (PowerShell)

1. Crie e ative um ambiente virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Instale dependências:

```powershell
pip install -r requirements.txt
```

3. Crie e aplique migrações:

```powershell
python manage.py makemigrations
python manage.py migrate
```

4. Crie um superuser:

```powershell
python manage.py createsuperuser
```

5. (Opcional) Popule dados de exemplo:

```powershell
python manage.py seed_data
```

6. Rode o servidor:

```powershell
python manage.py runserver
```

## Observações
- Atualize `LOJA_NUMERO` em `pedidos/views.py` com o número da loja (formato: código_pais + número, ex.: `5511999999999`).
- As páginas principais estão em `templates/pedidos/`.
- O carrinho é mantido na sessão (não persistido até finalizar).

## Comandos úteis
- `python manage.py shell` para abrir o shell do Django
- `python manage.py dumpdata pedidos > pedidos.json` para exportar dados do app

## Próximos passos que eu posso executar para você
- Adicionar testes unitários básicos.
- Preparar instruções de deploy (Heroku/Render/Railway).
- Ajustar validações ou melhorar UX.

Se quiser que eu execute algo mais, informe e eu continuo implementando.
Net Burger - Projeto Django (estrutura inicial)

Como usar:
1. criar virtualenv e ativar
2. pip install -r requirements.txt
3. python manage.py migrate
4. python manage.py createsuperuser
5. python manage.py runserver


