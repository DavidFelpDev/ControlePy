# Sistema de Controle de Estoque

Aplicacao desktop para cadastro e acompanhamento de materiais, com movimentacoes reais persistidas no PostgreSQL. A interface e feita em PySide6; as regras de negocio ficam em servicos Python e cada entrada ou saida e registrada junto com a atualizacao do saldo, na mesma transacao.

## Funcionalidades

- Autenticacao com hash PBKDF2-SHA256 e criacao do primeiro administrador no primeiro acesso.
- Perfis Administrador e Operador. O operador pode consultar o dashboard e registrar/consultar movimentacoes; cadastros e administracao ficam restritos ao administrador.
- Cadastro, pesquisa, edicao e exclusao de produtos e categorias.
- Entradas com fornecedor e saidas com responsavel e motivo.
- Protecao contra saldo negativo, quantidade nula/negativa e movimentacao de produto inativo.
- Historico com filtros por tipo, produto, usuario e periodo.
- Dashboard com totais, alertas de estoque minimo e movimentacoes recentes.
- PostgreSQL com chaves estrangeiras, restricoes, indices e operacoes transacionais.

## Tecnologias e requisitos

- Windows 10/11 (a interface tambem pode ser executada em outros sistemas suportados pelo Qt).
- Python 3.13 ou superior.
- PostgreSQL 14 ou superior.
- PySide6, psycopg 3, python-dotenv e PyInstaller.

## Instalacao

Abra o PowerShell nesta pasta do projeto e execute:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Se a politica do PowerShell impedir a ativacao do ambiente virtual, use `\.venv\Scripts\python.exe` no lugar de `python` nos comandos seguintes.

## Configurar PostgreSQL

1. Instale e inicie o servico PostgreSQL. Garanta que o cliente `psql` esteja disponivel no terminal.
2. Crie o banco (troque `postgres` pelo usuario administrador da sua instalacao, se necessario):

```powershell
psql -U postgres -c "CREATE DATABASE sistema_estoque ENCODING 'UTF8';"
```

3. Crie as tabelas, constraints e indices:

```powershell
psql -U postgres -d sistema_estoque -f database/schema.sql
```

O arquivo SQL cria as tabelas dentro do banco conectado. A criacao do banco e um comando separado porque `CREATE DATABASE` nao pode ser executado dentro da transacao que aplica o schema.

## Configurar ambiente

Copie o modelo e edite os valores locais:

```powershell
Copy-Item .env.example .env
notepad .env
```

Preencha `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER` e `DB_PASSWORD`. O `.env` e ignorado pelo Git. Nao distribua o arquivo com credenciais junto ao executavel.

## Executar e testar

```powershell
python main.py
```

Na primeira abertura, com o banco e o schema preparados, crie o administrador na propria tela de acesso. A senha deve ter pelo menos 10 caracteres. Depois, entre com essa conta e crie os operadores em **Usuarios**.

Execute os testes locais das validacoes sem precisar conectar ao banco:

```powershell
python -m unittest discover -s tests -v
```

Para validar uma movimentacao integrada, inicie a aplicacao, cadastre produto e categoria como administrador e registre entrada/saida pelas telas. O historico e o dashboard devem refletir o novo saldo. Uma saida maior que o saldo e rejeitada sem gravar alteracao.

## Gerar o executavel

Com as dependencias instaladas:

```powershell
pyinstaller --onefile --windowed --name SistemaEstoque main.py
```

O executavel sera criado em `dist\SistemaEstoque.exe`. A forma curta solicitada, `pyinstaller --onefile --windowed main.py`, tambem funciona, mas gera `dist\main.exe`.

Distribua o executavel sem credenciais e mantenha um `.env` configurado ao lado de `SistemaEstoque.exe`. O banco PostgreSQL e o schema devem estar previamente instalados no servidor. O arquivo SQL nao e embutido no executavel. Em ambientes de distribuicao, prefira um instalador que solicite a configuracao do banco e aplique o schema com credenciais administrativas adequadas.

## Estrutura

```text
database/       conexao PostgreSQL e schema SQL
models/         tipos de dominio
services/       autenticacao, catalogo, estoque e consultas
views/          login, dashboard e telas de operacao
utils/          validacoes, formatacao e mensagens
tests/          testes de validacao independentes do banco
main.py         inicializacao da aplicacao desktop
requirements.txt dependencias Python
```

## Notas de seguranca e consistencia

- Senhas de usuarios sao armazenadas como hashes PBKDF2 com salt aleatorio, nunca em texto puro.
- A senha do PostgreSQL fica em `.env`, fora do codigo-fonte.
- A movimentacao usa `SELECT ... FOR UPDATE` na linha do produto, atualiza o saldo e grava o historico na mesma transacao. Operacoes concorrentes sobre o mesmo produto sao serializadas.
- Exclusoes pedem confirmacao e chaves estrangeiras impedem apagar dados ainda referenciados.
- Mantenha backups regulares do PostgreSQL e proteja o arquivo `.env` e as credenciais do servidor.
