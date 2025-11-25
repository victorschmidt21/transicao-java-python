# Database Fixtures - Dados de Exemplo

Este diretório contém fixtures (dados de exemplo) para popular o banco de dados do sistema.

## Arquivos de Fixtures

### 1. **employees.json** - Funcionários
- **3 funcionários** cadastrados
- 1 Administrador (admin/admin@empresa.com)
- 2 Usuários regulares
- Senhas: `admin123` (você precisará criar com `createsuperuser` ou usar `loaddata`)

### 2. **suppliers.json** - Fornecedores
- **3 fornecedores** cadastrados
- Tech Solutions Ltda (SP)
- Distribuidora Alpha (RJ)
- Mega Informática (MG)

### 3. **customers.json** - Clientes
- **5 clientes** cadastrados
- Distribuídos em diferentes estados (SP, RJ, MG, PR, RS)
- Dados completos incluindo CPF, email, telefone e endereço

### 4. **products.json** - Produtos
- **10 produtos** cadastrados
- Periféricos (mouse, teclado, headset, webcam)
- Componentes (SSD, memória RAM, placa de vídeo)
- Equipamentos (notebook, impressora, monitor)
- Estoque variado (8 a 67 unidades)

### 5. **budgets.json** - Orçamentos
- **3 orçamentos** com seus itens
- Orçamento #1: 2 itens (R$ 1.049,70)
- Orçamento #2: 2 itens (R$ 4.298,00)
- Orçamento #3: 3 itens (R$ 1.948,90)

### 6. **orders.json** - Pedidos
- **3 pedidos** com seus itens
- Pedido #1: 2 itens (R$ 1.149,80)
- Pedido #2: 3 itens (R$ 1.588,90)
- Pedido #3: 1 item (R$ 579,80)

---

## Como Carregar as Fixtures

### Opção 1: Carregar Todas de Uma Vez (Recomendado)

```powershell
# No diretório raiz do projeto
python manage.py loaddata fixtures/suppliers.json
python manage.py loaddata fixtures/customers.json
python manage.py loaddata fixtures/products.json
python manage.py loaddata fixtures/budgets.json
python manage.py loaddata fixtures/orders.json
```

**Nota:** As fixtures de employees contêm senhas hasheadas que não funcionarão. Crie usuários manualmente ou use `createsuperuser`.

### Opção 2: Carregar Individualmente

```powershell
# Carregar apenas fornecedores
python manage.py loaddata fixtures/suppliers.json

# Carregar apenas clientes
python manage.py loaddata fixtures/customers.json

# Carregar apenas produtos
python manage.py loaddata fixtures/products.json

# Carregar apenas orçamentos
python manage.py loaddata fixtures/budgets.json

# Carregar apenas pedidos
python manage.py loaddata fixtures/orders.json
```

### Opção 3: Usar o Script Automatizado

```powershell
# Executar o script que carrega tudo na ordem correta
python load_fixtures.py
```

---

## Ordem de Carregamento

**IMPORTANTE:** As fixtures devem ser carregadas nesta ordem devido às dependências:

1. ✅ **suppliers** (não tem dependências)
2. ✅ **customers** (não tem dependências)
3. ✅ **products** (depende de suppliers)
4. ✅ **budgets** (depende de customers e products)
5. ✅ **orders** (depende de customers e products)

---

## Resetar o Banco de Dados

Se você quiser começar do zero:

```powershell
# Deletar o banco de dados
Remove-Item db.sqlite3

# Recriar as tabelas
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Carregar as fixtures
python manage.py loaddata fixtures/suppliers.json
python manage.py loaddata fixtures/customers.json
python manage.py loaddata fixtures/products.json
python manage.py loaddata fixtures/budgets.json
python manage.py loaddata fixtures/orders.json
```