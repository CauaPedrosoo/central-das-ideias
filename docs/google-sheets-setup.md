# Google Sheets Setup

## O que voce vai precisar

- uma planilha Google Sheets vazia;
- o `spreadsheet_id` da URL da planilha;
- uma service account no Google Cloud com acesso ao Google Sheets API;
- o JSON da service account.

## Passo 1: criar a planilha

Crie uma planilha no Google Sheets. Sugestao de nome:

`Central das Ideias`

Copie o ID da URL:

`https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit`

## Passo 2: criar a service account

1. Entre no Google Cloud Console.
2. Crie ou selecione um projeto.
3. Ative a `Google Sheets API`.
4. Va em `IAM e Admin` -> `Service Accounts`.
5. Crie uma service account.
6. Gere uma chave JSON para ela.

## Passo 3: compartilhar a planilha

Pegue o email da service account, algo como:

`nome-da-conta@projeto.iam.gserviceaccount.com`

Compartilhe a planilha com esse email como `Editor`.

## Passo 4: configurar variaveis

Voce pode usar uma destas opcoes:

### Opcao A: arquivo JSON

Crie um `.env` no repo com:

```env
GOOGLE_SHEETS_SPREADSHEET_ID=seu_spreadsheet_id
GOOGLE_SERVICE_ACCOUNT_FILE=C:\caminho\para\service-account.json
```

### Opcao B: JSON inline

Crie um `.env` no repo com:

```env
GOOGLE_SHEETS_SPREADSHEET_ID=seu_spreadsheet_id
GOOGLE_SERVICE_ACCOUNT_JSON={"type":"service_account","project_id":"..."}
```

Para automacao cloud, a segunda opcao tende a ser mais pratica se voce for configurar secrets/env vars no ambiente da automacao.

## Passo 5: bootstrap

Quando as variaveis estiverem prontas:

```bash
pip install -r requirements.txt
python scripts/sheets_sync.py bootstrap
```

Isso cria e popula as abas:

- `content_ideas`
- `lead_assets`

## Passo 6: snapshot opcional

Para baixar um retrato atual da planilha:

```bash
python scripts/sheets_sync.py snapshot
```

## Passo 7: upsert

Para sincronizar os CSVs locais com a planilha sem apagar a base inteira:

```bash
python scripts/sheets_sync.py upsert
```

## Fluxo recomendado para automacao cloud

1. Baixar o estado atual da planilha:

```bash
python scripts/sheets_sync.py snapshot
```

2. Editar apenas os arquivos em `data/runtime/`.

3. Enviar as mudancas de volta:

```bash
python scripts/sheets_sync.py upsert-runtime
```

Esse fluxo evita que a automacao precise alterar os CSVs seed versionados no repositorio.
