# Configuração MCP - Google Sheets + Antigravity

## 📋 Visão Geral

Este servidor MCP automatiza a sincronização de produtos entre sua planilha Google Sheets e seu site via Antigravity. Cada vez que você adiciona um novo produto à planilha, o sistema:

1. ✅ Lê o produto da planilha
2. ✅ Sincroniza com Antigravity
3. ✅ Atualiza automaticamente seu repositório
4. ✅ Publica as mudanças no site

---

## 🔧 Pré-requisitos

- Node.js v18+
- Uma planilha no Google Sheets
- Conta no Antigravity
- GitHub Copilot habilitado

---

## 📝 Passo 1: Configurar Google Sheets

### 1.1 Criar Planilha

Crie uma planilha com as seguintes colunas:

| Nome | URL Mercado Livre | Preço | Descrição | Categoria | Ativo |
|------|-------------------|-------|-----------|-----------|-------|
| Produto 1 | https://ml.com/... | 99.90 | Descrição | Eletrônicos | Sim |
| Produto 2 | https://ml.com/... | 149.90 | Descrição | Roupas | Sim |

### 1.2 Gerar Credenciais Google

1. Acesse [Google Cloud Console](https://console.cloud.google.com)
2. Crie um novo projeto
3. Ative a API "Google Sheets API"
4. Crie uma chave de API
5. Copie seu `GOOGLE_SHEETS_ID` da URL: `https://docs.google.com/spreadsheets/d/**SEU_ID_AQUI**/edit`

---

## 🌐 Passo 2: Configurar Antigravity

1. Acesse sua conta Antigravity
2. Vá para Configurações → API
3. Gere uma nova chave de API
4. Copie `ANTIGRAVITY_API_KEY` e `ANTIGRAVITY_API_URL`

---

## ⚙️ Passo 3: Configurar Variáveis de Ambiente

### 3.1 Criar arquivo `.env`

```bash
cp .env.example .env
```

### 3.2 Preencher `.env`

```
GOOGLE_SHEETS_ID=sua_planilha_id_aqui
GOOGLE_API_KEY=sua_chave_api_google_aqui
ANTIGRAVITY_API_KEY=sua_chave_api_antigravity_aqui
ANTIGRAVITY_API_URL=https://api.antigravity.com
REPO_PATH=./
```

---

## 📦 Passo 4: Instalar Dependências

```bash
npm install
```

---

## ▶️ Passo 5: Habilitar MCP no GitHub Copilot

1. Acesse: https://github.com/psicopoeta/Achados-4u/settings/copilot/mcp
2. Clique em "Add MCP Server"
3. Selecione **google-sheets-antigravity-sync**
4. Configure com suas credenciais
5. Clique em "Enable"

---

## 🚀 Passo 6: Testar Sincronização

### Opção 1: Via terminal

```bash
npm run sync
```

### Opção 2: Via GitHub Copilot

Abra uma chat com o Copilot e peça:

> "Sincronize os produtos da planilha Google Sheets para o site"

---

## 📊 Ferramentas Disponíveis no MCP

### 1. `read_google_sheets`
Lê todos os produtos da planilha.

**Exemplo de saída:**
```json
[
  {
    "nome": "Produto 1",
    "url_mercado_livre": "https://...",
    "preco": 99.90,
    "descricao": "Descrição...",
    "categoria": "Eletrônicos",
    "ativo": true
  }
]
```

### 2. `sync_product_to_antigravity`
Sincroniza um produto específico com Antigravity.

### 3. `update_repository`
Atualiza os arquivos do repositório com os produtos sincronizados.

### 4. `get_sync_status`
Retorna informações sobre a última sincronização.

---

## 🔄 Fluxo Automático

```
Planilha Google Sheets
    ↓
MCP Server lê dados
    ↓
Valida produtos
    ↓
Envia para Antigravity
    ↓
Atualiza arquivos do repositório
    ↓
Site é publicado automaticamente
```

---

## 📁 Estrutura de Arquivos Gerados

```
Achados-4u/
├── data/
│   └── produtos.json          # JSON com todos os produtos
├── public/
│   └── produtos.html          # HTML renderizado
├── scripts/
│   └── mcp-server-google-sheets.js
├── .vscode/
│   └── mcp.json               # Configuração MCP
├── .env                       # Variáveis de ambiente
└── .mcp-sync-status.json      # Status da última sincronização
```

---

## 🐛 Troubleshooting

### Erro: "GOOGLE_API_KEY não definida"
- Verifique se o arquivo `.env` está criado
- Confirme se as variáveis estão preenchidas corretamente

### Erro: "Antigravity API não respondeu"
- Verifique se a chave de API está correta
- Confirme se a URL da API está acessível
- Valide se sua conta Antigravity está ativa

### Erro: "Planilha não encontrada"
- Copie corretamente o `GOOGLE_SHEETS_ID` da URL
- Verifique se você tem permissão de acesso à planilha

---

## 💡 Dicas

- **Sincronizar manualmente:** Use `npm run sync` no terminal
- **Monitorar alterações:** Use `npm run dev` para modo desenvolvimento
- **Limpar cache:** Delete `.mcp-sync-status.json`

---

## 📞 Suporte

Para dúvidas ou problemas, abra uma issue no repositório!
