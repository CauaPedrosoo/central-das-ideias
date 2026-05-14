# Central das Ideias

Base para capturar, estruturar e sincronizar noticias e ideias de conteudo sobre inteligencia artificial.

## Objetivo

Este repositorio existe para:

- manter uma fila de noticias relevantes sobre IA;
- manter um banco de ideias sobre IA aplicada;
- registrar lead magnets e CTAs;
- sincronizar a base com Google Sheets;
- permitir que automacoes locais do Codex atualizem o banco na nuvem.

Nesta fase, a automacao nao monta calendario editorial. Ela pesquisa, filtra e guarda as noticias mais importantes sem repetir fatos.

## Estrutura

- `data/news_intake.csv`: seed inicial e fallback local da fila de noticias.
- `data/content_ideas.csv`: seed inicial e fallback local do banco de ideias.
- `data/lead_assets.csv`: seed inicial e fallback local dos lead magnets.
- `docs/google-sheets-setup.md`: passo a passo para conectar a planilha.
- `prompts/automation_brief.md`: regras editoriais da automacao.
- `scripts/sheets_sync.py`: CLI para bootstrap, snapshot e upsert no Google Sheets.
- `src/central_das_ideias/sheets_store.py`: integracao Python com Google Sheets.

## Modelo de abas no Google Sheets

- `news_intake`
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

6. Para baixar um snapshot atual da planilha para inspecao local:

```bash
python scripts/sheets_sync.py snapshot
```

7. Para o fluxo da automacao, edite apenas os arquivos em `data/runtime/` e depois sincronize de volta:

```bash
python scripts/sheets_sync.py upsert-runtime
```

## Como a automacao deve operar

1. Ler `prompts/automation_brief.md`.
2. Rodar `python scripts/sheets_sync.py snapshot`.
3. Consultar obrigatoriamente as paginas:
   - `https://exame.com/inteligencia-artificial/`
   - `https://www.cnnbrasil.com.br/tudo-sobre/inteligencia-artificial/`
   - `https://www.infomoney.com.br/tudo-sobre/inteligencia-artificial/`
4. Consultar tambem fontes complementares relevantes de IA, incluindo blogs oficiais de empresas e publicacoes fortes do setor.
5. Atualizar `data/runtime/news_intake.csv` com exatamente 10 noticias relevantes por rodada, escolhidas do conjunto total de fontes.
6. Nao repetir noticia ja capturada. Dedupe por `article_url`, manchete e fato principal.
7. Opcionalmente atualizar `content_ideas` e `lead_assets` quando houver um gancho realmente forte.
8. Rodar `python scripts/sheets_sync.py upsert-runtime`.
9. Nao criar datas de postagem nesta fase.

## Aba de noticias

`news_intake` guarda o intake bruto da automacao. Campos:

- `news_id`
- `captured_at`
- `source_name`
- `source_index_url`
- `article_url`
- `headline`
- `published_label`
- `category`
- `importance_score`
- `importance_reason`
- `summary`
- `content_angle`
- `audience_segment`
- `status`
- `dedupe_key`
- `notes`

## Status sugeridos

- `captured`
- `reviewed`
- `approved`
- `drafting`
- `published`
- `discarded`
