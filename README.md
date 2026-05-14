# Central das Ideias

Base para capturar, estruturar e sincronizar ideias de conteudo sobre inteligencia artificial.

## Objetivo

Este repositorio existe para:

- manter um banco de ideias sobre IA aplicada;
- registrar lead magnets e CTAs;
- sincronizar a base com Google Sheets;
- permitir que automacoes do Codex rodem em nuvem sem depender do app aberto.

Nesta fase, a automacao nao monta calendario editorial. Ela so pesquisa, filtra e guarda ideias boas.

## Estrutura

- `data/content_ideas.csv`: seed inicial e fallback local do banco de ideias.
- `data/lead_assets.csv`: seed inicial e fallback local dos lead magnets.
- `docs/google-sheets-setup.md`: passo a passo para conectar a planilha.
- `prompts/automation_brief.md`: regras editoriais da automacao.
- `scripts/sheets_sync.py`: CLI para bootstrap, snapshot e upsert no Google Sheets.
- `src/central_das_ideias/sheets_store.py`: integracao Python com Google Sheets.

## Modelo de abas no Google Sheets

- `content_ideas`
- `lead_assets`

## Setup

1. Crie uma planilha Google Sheets.
2. Compartilhe a planilha com o email da service account do Google.
3. Configure as variaveis abaixo em um `.env` local ou no ambiente da automacao:

`GOOGLE_SHEETS_SPREADSHEET_ID`

Uma das duas opcoes abaixo:

`GOOGLE_SERVICE_ACCOUNT_JSON`

ou

`GOOGLE_SERVICE_ACCOUNT_FILE`

4. Instale dependencias:

```bash
pip install -r requirements.txt
```

5. Rode o bootstrap inicial:

```bash
python scripts/sheets_sync.py bootstrap
```

6. Se quiser baixar um snapshot atual da planilha para inspeção local:

```bash
python scripts/sheets_sync.py snapshot
```

7. Para o fluxo de automacao em nuvem, use:

```bash
python scripts/sheets_sync.py snapshot
```

Edite apenas os arquivos em `data/runtime/` e depois sincronize de volta:

```bash
python scripts/sheets_sync.py upsert-runtime
```

## Como a automacao deve operar

1. Ler `prompts/automation_brief.md`.
2. Consultar o estado atual do banco no Google Sheets.
3. Pesquisar temas recentes e ideias evergreen.
4. Baixar snapshot para `data/runtime/`.
5. Adicionar ate 5 ideias novas, sem duplicar angulos, editando os CSVs de runtime.
6. Se surgir um novo lead magnet valido, adicionar em `lead_assets` de runtime.
7. Executar `upsert-runtime` para devolver as mudancas ao Sheets.
6. Nao criar datas de postagem nesta fase.

## Status sugeridos

- `captured`
- `approved`
- `drafting`
- `scheduled`
- `published`
- `discarded`
