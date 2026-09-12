import os
import re
import json
import sys
import unicodedata
import urllib.request
import urllib.parse

CHAVE_API = os.environ.get("GOOGLE_API_KEY", "")
LINK_OU_ID_PLANILHA = "https://docs.google.com/spreadsheets/d/1l_-h10C6XhYJ7wlM0MIOHVY0HjlXF8gPmNfSmiGDVsA/edit?usp=sharing"

ABAS_PROJETO = [
    "REGULAÇÃO SENSORIAL",
    "PROPRIOCEPÇÃO E VESTIBULAR",
    "PEDAGOGICO E COGNITIVO",
    "POSTURA E MOTRICIDADE"
]

# Nomes de coluna aceitos por campo
COLUNAS = {
    "id":            ["ID"],
    "categoria":     ["CATEGORIA"],
    "nome":          ["NOME", "PRODUTO", "TITULO", "TÍTULO"],
    "link_afiliado": ["URL_LINK_PROD", "LINK PROD", "LINK"],
    "preco_atual":   ["PREÇO PROMO", "PRECO PROMO", "PREÇO_PROMO"],
    "preco_antigo":  ["PREÇO REAL", "PRECO REAL", "PREÇO_REAL"],
    "url_imagem":    ["URL_IMG", "URL_FOTO", "FOTO", "MIDIA", "MÍDIA", "IMAGEM"]
}

# Fallback posicional corrigido com base na estrutura real da planilha
FALLBACK = {
    "id": 0, 
    "categoria": 1, 
    "nome": 2, 
    "link_afiliado": 3,
    "url_imagem": 4,
    "preco_atual": 5, 
    "preco_antigo": 6
}

def normalizar_nome_coluna(texto):
    """Remove acentos, espaços extras e padroniza em maiúsculas."""
    if not texto:
        return ""
    texto = re.sub(r"\s+", " ", texto).strip().upper()
    return "".join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )

def extrair_id_valido(valor):
    m = re.search(r'/d/([a-zA-Z0-9-_]+)', valor)
    return m.group(1) if m else valor.strip()

def achar_indice(cabecalho, possiveis, fallback):
    cabecalho_normalizado = [
        normalizar_nome_coluna(col)
        for col in cabecalho
    ]

    for nome in possiveis:
        nome_normalizado = normalizar_nome_coluna(nome)

        if nome_normalizado in cabecalho_normalizado:
            return cabecalho_normalizado.index(nome_normalizado)

    print(
        f"   ⚠️ Coluna não encontrada para "
        f"{possiveis}, usando posição {fallback}"
    )
    return fallback

def celula(linha, i):
    return linha[i].strip() if 0 <= i < len(linha) else ""

def baixar_dados_planilha():
    chave = CHAVE_API.strip()

    if not chave:
        print("❌ Defina a variável de ambiente GOOGLE_API_KEY.")
        sys.exit(1)

    id_planilha = extrair_id_valido(LINK_OU_ID_PLANILHA)
    produtos = []

    for nome_aba in ABAS_PROJETO:
        print(f"Buscando dados da aba: {nome_aba}...")

        aba_codificada = urllib.parse.quote(nome_aba.strip())

        url = (
            f"https://sheets.googleapis.com/v4/spreadsheets/"
            f"{id_planilha}/values/{aba_codificada}?key={chave}"
        )

        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "Mozilla/5.0"}
            )

            with urllib.request.urlopen(req) as resp:
                dados = json.loads(resp.read().decode("utf-8"))

            linhas = dados.get("values", [])

        except Exception as e:
            print(f"⚠️ Não foi possível ler a aba {nome_aba}: {e}")
            continue

        if len(linhas) <= 1:
            print("   Aba vazia.")
            continue

        cabecalho = linhas[0]

        idx = {
            campo: achar_indice(
                cabecalho,
                nomes,
                FALLBACK[campo]
            )
            for campo, nomes in COLUNAS.items()
        }

        for linha in linhas[1:]:
            # Garante que a linha tenha colunas suficientes para não dar IndexError
            tamanho_maximo = max(idx.values()) + 1
            if len(linha) < tamanho_maximo:
                linha = list(linha) + [""] * (tamanho_maximo - len(linha))

            link = celula(linha, idx["link_afiliado"])

            # Valida se a célula realmente contém um link válido
            if not re.match(r"^https?://", link, re.IGNORECASE):
                continue

            produtos.append({
                "id": celula(linha, idx["id"]),
                "categoria": celula(linha, idx["categoria"]).upper(),
                "nome": celula(linha, idx["nome"]),
                "link_afiliado": link,
                "preco_atual": celula(linha, idx["preco_atual"]),
                "preco_antigo": celula(linha, idx["preco_antigo"]),
                "url_imagem": celula(linha, idx["url_imagem"])
            })

    if produtos:
        with open("produtos.json", "w", encoding="utf-8") as f:
            json.dump(produtos, f, ensure_ascii=False, indent=2)
        print(f"\n✅ SUCESSO! produtos.json gerado com {len(produtos)} produtos!")
    else:
        print("\n⚠️ Nenhum produto válido encontrado.")
        sys.exit(1)

if __name__ == "__main__":
    baixar_dados_planilha()

