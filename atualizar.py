import os
import json
import urllib.request
import urllib.parse
import re

# CONFIGURAÇÕES ADAPTADAS PARA A SUA PLANILHA REAL
CHAVE_API = "AIzaSyCOw0sef-Alux79-MuoQtH6oM525GVOC6g"
LINK_OU_ID_PLANILHA = "https://docs.google.com/spreadsheets/d/1l_-h10C6XhYJ7wlM0MIOHVY0HjlXF8gPmNfSmiGDVsA/edit?usp=sharing"
NOME_ABA = "REGULATEA" # Ajustado para o nome da sua aba do print anterior

def extrair_id_valido(valor):
    if "://google.com" in valor:
        match = re.search(r'/d/([a-zA-Z0-9-_]+)', valor)
        if match:
            return match.group(1).strip()
    return valor.strip()

def baixar_dados_planilha():
    id_planilha_limpo = extrair_id_valido(LINK_OU_ID_PLANILHA)
    chave_limpa = CHAVE_API.strip()
    aba_codificada = urllib.parse.quote(NOME_ABA.strip())
    
    url = f"https://googleapis.com{id_planilha_limpo}/values/{aba_codificada}?key={chave_limpa}"
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            dados = json.loads(response.read().decode('utf-8'))
            linhas = dados.get('values', [])
            
            if not linhas or len(linhas) <= 1:
                print("Planilha vazia ou sem dados cadastrados.")
                return
            
            produtos_lista = []
            
            # Varre a planilha pulando a linha 1 (Título) e linha 2 (Cabeçalho)
            for linha in linhas[2:]:
                # Evita ler linhas totalmente vazias ou IDs sem link cadastrado
                if len(linha) < 4 or not linha[2]: 
                    continue
                
                # Se você criar a coluna de Imagem no futuro, o script coleta ela na posição 8
                url_img = linha[8] if len(linha) > 8 and linha[8] else "img/placeholder.png"
                
                produto = {
                    "id": linha[0],                             # ID
                    "categoria": linha[1],                      # CATEGORIA
                    "link_afiliado": linha[2],                  # LINK PROD
                    "preco_atual": linha[3],                    # PREÇO PROMO
                    "preco_antigo": linha[4] if linha[4] else "",# PREÇO REAL
                    "url_imagem": url_img                       # URL extraída
                }
                produtos_lista.append(produto)
            
            with open("produtos.json", "w", encoding="utf-8") as f:
                json.dump(produtos_lista, f, ensure_ascii=False, indent=2)
            print("\n✅ SUCESSO! O arquivo produtos.json foi gerado com as colunas em português!")
            
    except Exception as e:
        print(f"\n❌ Erro crítico no processamento: {e}")

if __name__ == "__main__":
    baixar_dados_planilha()
