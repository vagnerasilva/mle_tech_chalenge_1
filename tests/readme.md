# Testes Unitários e de Integração

Este diretório contém a suite completa de testes para o projeto MLE Tech Challenge 1.

## Estrutura dos Testes

### `conftest.py`
Configuração centralizada de fixtures pytest. Fornece:
- `test_db`: Banco de dados SQLite em memória isolado para cada teste
- `client`: Cliente TestClient FastAPI com dependências mockadas
- `sample_category`: Categoria de teste padrão ("Fiction")
- `sample_book`: Livro de teste padrão com todas as propriedades
- `multiple_books`: Lista de 5 livros com preços e ratings variados

### `test_models.py`
Testes para modelos SQLAlchemy (ORM) e schemas Pydantic:
- **TestCategoryModel**: Validação de criação, string representation, constraint de unicidade
- **TestBookModel**: Validação de campos, constraints (rating 0-5, UPC único), relacionamentos
- **TestBookSchema & TestCategorySchema**: Conversão ORM → Pydantic, serialização

**Cobertura**: 100% dos modelos

### `test_services.py`
Testes para lógica de negócio (camada de serviços):
- **TestBookService**: 
  - Operações CRUD (get_books, get_book, filter_books)
  - Filtros complexos (preços, títulos)
  - Validação de erros (intervalo de preço inválido)
- **TestCategoryService**: Obtenção e listagem de categorias
- **TestStatsService**: Cálculo de estatísticas agregadas (overview, por categoria)

**Cobertura**: 70%+ dos serviços

### `test_routers.py`
Testes para endpoints FastAPI:
- **TestPublicRoutes**: Home e login (sem autenticação obrigatória)
- **Skipped Tests**: Endpoints protegidos por AuthMiddleware requerem sessão válida

**Nota**: A maioria dos endpoints está marcada como `@skip` pois o aplicativo usa `AuthMiddleware` que requer autenticação GitHub. Para testar endpoints autenticados, seria necessário:
1. Mockar o AuthMiddleware
2. Adicionar rotas de teste à lista pública em `app/services/auth_middleware.py`
3. Implementar fixture que fornece access_token válido

## Executar Testes

### Todos os testes
```bash
pytest tests/ -v
```

### Testes específicos
```bash
# Apenas modelos
pytest tests/test_models.py -v

# Apenas serviços
pytest tests/test_services.py -v

# Apenas routers
pytest tests/test_routers.py -v

# Teste específico
pytest tests/test_models.py::TestBookModel::test_create_book -v
```

### Com cobertura
```bash
pytest tests/ --cov=app --cov-report=html
# Abre htmlcov/index.html para visualizar relatório detalhado
```

### Modo watch (reexecuta ao mudar arquivos)
```bash
pytest tests/ --looponfail
```

## Configuração

### `pytest.ini`
Define comportamento padrão:
- Descoberta automática de testes em `tests/`
- Padrão de nomeação: `test_*.py` e `Test*` classes
- Output verbose com traceback curto
- Marcadores customizados para categorizar testes

### `requirements-dev.txt`
Dependências de desenvolvimento:
- `pytest`: Framework de testes
- `pytest-cov`: Plugin de cobertura
- `pytest-asyncio`: Suporte a testes async
- `httpx`: Cliente HTTP (usado por TestClient)

### Instalação
```bash
pip install -r requirements-dev.txt
```

## Cobertura Atual

**Resumo**: 66% da base de código testada (28 testes passando)

**Por módulo**:
- Modelos: 100%
- Estatísticas: 100%
- Configurações: 100%
- Serviços: 72% (excluindo scraping)
- Routers: 29-90% (limitado por AuthMiddleware)
- Middleware: 43%

**Ausente de testes**:
- `scraping.py`: Requer requisições HTTP reais para sites
- `auth_middleware.py`: Requer GitHub OAuth mocking complexo
- Endpoints protegidos: Requeriam fixture de autenticação

## Exemplo de Teste

```python
def test_get_books_between_prices(self, test_db, multiple_books):
    """Testa filtro de intervalo de preços."""
    books = get_books_between_prices(db=test_db, min=15.0, max=25.0)
    
    assert len(books) == 3
    for book in books:
        assert 15.0 <= book.price_incl_tax <= 25.0
```

## Melhorias Futuras

1. **Mockar AuthMiddleware**: Permitir testes de endpoints autenticados
2. **Testes de integração**: Usar banco de dados real temporário
3. **Load testing**: pytest-benchmark para testes de performance
4. **Snapshot testing**: pytest-snapshot para validar respostas complexas
5. **API contract testing**: Validar schemas com pydantic
