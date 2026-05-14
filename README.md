# Central das Ideias

Base para capturar, estruturar e sincronizar noticias, contexto editorial e criativos sobre inteligencia artificial.

## Objetivo

Este repositorio existe para:

- manter uma fila de noticias relevantes sobre IA;
- transformar noticias aprovadas em contexto estruturado;
- gerar briefings e rascunhos de criativos com contexto suficiente;
- registrar lead magnets e CTAs;
- sincronizar a base com Google Sheets;
- permitir que automacoes locais do Codex atualizem o banco na nuvem.

O fluxo foi dividido em duas camadas:

1. coleta de noticias;
2. enriquecimento de contexto e geracao de criativos.

## Estrutura

- `data/news_intake.csv`: seed inicial e fallback local da fila de noticias.
- `data/context_enrichment.csv`: contexto estruturado por noticia aprovada.
- `data/creative_outputs.csv`: briefs e rascunhos de criativos por contexto.
- `data/content_ideas.csv`: banco de ideias derivadas.
- `data/lead_assets.csv`: lead magnets e CTAs.
- `docs/google-sheets-setup.md`: passo a passo para conectar a planilha.
- `prompts/automation_brief.md`: regras da automacao de coleta.
- `prompts/creative_automation_brief.md`: regras da automacao de contexto e criativos.
- `scripts/sheets_sync.py`: CLI para bootstrap, snapshot e upsert no Google Sheets.
- `src/central_das_ideias/sheets_store.py`: integracao Python com Google Sheets.

## Modelo de abas no Google Sheets

- `news_intake`
- `context_enrichment`
- `creative_outputs`
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

7. Para o fluxo das automacoes, edite apenas os arquivos em `data/runtime/` e depois sincronize de volta:

```bash
python scripts/sheets_sync.py upsert-runtime
```

## Fluxo 1: Noticias

1. Ler `prompts/automation_brief.md`.
2. Rodar `python scripts/sheets_sync.py snapshot`.
3. Consultar obrigatoriamente:
   - `https://exame.com/inteligencia-artificial/`
   - `https://www.cnnbrasil.com.br/tudo-sobre/inteligencia-artificial/`
   - `https://www.infomoney.com.br/tudo-sobre/inteligencia-artificial/`
4. Consultar tambem fontes complementares relevantes de IA.
5. Atualizar `data/runtime/news_intake.csv` com exatamente 10 noticias relevantes por rodada.
6. Nao repetir noticia ja capturada. Dedupe por `article_url`, manchete e fato principal.
7. Rodar `python scripts/sheets_sync.py upsert-runtime`.

## Fluxo 2: Contexto e Criativos

1. Marque em `news_intake` as noticias que quer transformar em conteudo com `status=approved`.
2. A automacao de criativos le `prompts/creative_automation_brief.md`.
3. Ela roda `python scripts/sheets_sync.py snapshot`.
4. Para cada noticia `approved` sem contexto, ela cria uma linha em `context_enrichment`.
5. Para cada contexto `ready_for_creative`, ela cria ou atualiza linhas em `creative_outputs`.
6. Ela tambem pode registrar ideias derivadas em `content_ideas` e CTAs ou iscas em `lead_assets`.
7. Por fim, roda `python scripts/sheets_sync.py upsert-runtime`.

## Aba de noticias

`news_intake` guarda o intake bruto. Campos:

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

## Aba de contexto

`context_enrichment` guarda o pacote que a IA deve usar para criar conteudo. Campos:

- `context_id`
- `news_id`
- `article_url`
- `source_name`
- `headline`
- `main_claim`
- `key_facts_json`
- `numbers_json`
- `who_is_affected`
- `why_it_matters`
- `practical_takeaway`
- `risks_or_limitations`
- `audience_fit`
- `content_angles_json`
- `cta_opportunities_json`
- `recommended_formats`
- `status`
- `notes`

## Aba de criativos

`creative_outputs` guarda briefs e rascunhos por formato. Campos:

- `creative_id`
- `context_id`
- `news_id`
- `platform`
- `format`
- `working_title`
- `hook`
- `creative_brief`
- `structure`
- `caption`
- `cta`
- `asset_suggestion`
- `status`
- `generated_at`
- `notes`

## Status sugeridos

- `captured`
- `reviewed`
- `approved`
- `context_ready`
- `ready_for_creative`
- `drafting`
- `published`
- `discarded`
