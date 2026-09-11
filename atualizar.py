import os
import json
import urllib.request
import urllib.parse
import re

A chave agora vem de variável de ambiente (nunca hardcode!)
CHAVE_API = os.environ.get("GOOGLE_API_KEY", "")
LINK_OU_ID_PLANILHA = "https://docs.google.com/spreadsheets/d/1l_-h10C6XhYJ7wlM0MIOHVY0HjlXF8gPmNfSmiGDVsA/edit?usp=sharing"

ABAS_PROJETO = [
"REGULAÇÃO SENSORIAL",
"PROPRIOCEPÇÃO E VESTIBULAR",
"PEDAGOGICO E COGNITIVO",
"POSTURA E MOTRICIDADE"
]

def extrair_id_valido(valor):
match = re.search(r'/d/([a-zA-Z0-9-_]+)', valor)
if match:
return match.group(1)
return valor.strip()

def baixar_dados_planilha():
id_planilha_limpo = extrair_id_valido(LINK_OU_ID_PLANILHA)
chave_limpa = CHAVE_API.strip()

if not chave_limpa:
print("❌ Defina a variável de ambiente GOOGLE_API_KEY.")
return

produtos_consolidados = []

for nome_aba in ABAS_PROJETO:
print(f"Buscando dados da aba: {nome_aba}...")
aba_codificada = urllib.parse.quote(nome_aba.strip())

url = f"https://sheets.googleapis.com/v4/spreadsheets/{id_planilha_limpo}/values/{aba_codificada}?key={chave_limpa}"

try:
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as response:
dados = json.loads(response.read().decode('utf-8'))
linhas = dados.get('values', [])

if not linhas or len(linhas) <= 1:
print(f"Aba {nome_aba} está vazia.")
continue

cabecalho = [col.strip().upper() for col in linhas[0]]

idx_id = cabecalho.index("id") if "id" in cabecalho else 0
idx_categoria = cabecalho.index("categoria") if "categoria" in cabecalho else 1
idx_id = cabecalho.index("nome") if "nome" in cabecalho else 2
idx_link = cabecalho.index("url_link_prod") if "url_link_prod" in cabecalho else 3
idx_img = cabecalho.index("url_foto") if "url_foto" in cabecalho else 4
idx_promo = cabecalho.index("preco_promo") if "preco_promo" in cabecalho else 5
idx_real = cabecalho.index("preco_real") if "preco_real" in cabecalho else 6

for linha in linhas[1:]:
if not linha or len(linha) <= max(idx_id, idx_categoria):
continue

while len(linha) < len(cabecalho):
linha.append("")

url_link_prod = linha[idx_link].strip() if idx_link < len(linha) else ""
if not link_afiliado:
continue

produtos_consolidados.append({
"id": linha[idx_id].strip(),
"categoria": linha[idx_categoria].strip().upper(),
"nome": linha[idx_id].strip(),
"url_link_prod": link_afiliado,
"preco_promo": linha[idx_promo].strip() or "0.00",
"preco_antigo": linha[idx_real].strip(),
"url_foto": linha[idx_img].strip()
})
except Exception as e:
print(f"⚠️ Não foi possível ler a aba {nome_aba}: {e}")
continue

if produtos_consolidados:
with open("produtos.json", "w", encoding="utf-8") as f:
json.dump(produtos_consolidados, f, ensure_ascii=False, indent=2)
print(f"\n✅ SUCESSO! produtos.json gerado com {len(produtos_consolidados)} produtos!")
else:
print("\n⚠️ Nenhum produto válido encontrado.")

if name == "main":
baixar_dados_planilha()
