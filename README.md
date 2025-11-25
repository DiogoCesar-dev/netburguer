# NetBurger

Sistema NetBurger - cardápio online com envio via WhatsApp

## Pré-requisitos
- Python 3.8+
- Virtualenv (recomendado)

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

Observações:
- Ajuste LOJA_NUMERO em pedidos/views.py para o número desejado (DDI+DDD+Número).
- As páginas principais estão em templates/pedidos/.
- Carrinho usa sessão e não é persistido até finalizar o pedido.
