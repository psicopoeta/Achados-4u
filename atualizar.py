import os
import json
import urllib.request
import urllib.parse
import re

# CONFIGURAÇÕES DA SUA AUTOMAÇÃO
CHAVE_API = "AIzaSyCOw0sef-Alux79-MuoQtH6oM525GVOC6g"  # Substitua pela sua chave secreta do Google Cloud
LINK_OU_ID_PLANILHA = "https://docs.google.com/spreadsheets/d/1l_-h10C6XhYJ7wlM0MIOHVY0HjlXF8gPmNfSmiGDVsA/edit?usp=sharing"  # Cole o link da sua planilha aqui

# Lista exata com o nome das 4 abas que você criou na planilha
ABAS_PROJETO = [
    "REGULAÇÃO SENSORIAL",
    "PROPRIOCEPÇÃO VESTIBULAR",
    "PEDAGOGICO E COGNITIVO",
    "POSTURA E MOTRICIDADE"
]

def extrair_id_valido(valor):
    if "://google.com" in valor:
        match = re.search(r'/d/([a-zA-Z0-9-_]+)', valor)
        if match:
            return match.group(1).strip()
    return valor.strip()

def baixar_dados_planilha():
    id_planilha_limpo = extrair_id_valido(LINK_OU_ID_PLANILHA)
    chave_limpa = CHAVE_API.strip()
    
    produtos_consolidados = []
    
    # O robô agora varre cada uma das abas sequencialmente
    for nome_aba in ABAS_PROJETO:
        print(f"Buscando dados da aba: {nome_aba}...")
        aba_codificada = urllib.parse.quote(nome_aba.strip())
        
        url = f"https://googleapis.com{id_planilha_limpo}/values/{aba_codificada}?key={chave_limpa}"
        
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                dados = json.loads(response.read().decode('utf-8'))
                linhas = dados.get('values', [])
                
                # Verifica se a aba tem o cabeçalho e pelo menos 1 produto cadastrado
                if not linhas or len(linhas) <= 1:
                    print(f"Aba {nome_aba} está vazia ou sem produtos cadastrados.")
                    continue
                
                # Localiza a posição de cada coluna dinamicamente para evitar quebras por espaços extras
                cabecalho = [col.strip().upper() for col in linhas[0]]
                
                idx_id = cabecalho.index("ID") if "ID" in cabecalho else 0
                idx_categoria = cabecalho.index("CATEGORIA") if "CATEGORIA" in cabecalho else 1
                idx_link = cabecalho.index("URL_LINK_PROD") if "URL_LINK_PROD" in cabecalho else 2
                idx_promo = cabecalho.index("PREÇO PROMO") if "PREÇO PROMO" in cabecalho else 3
                idx_real = cabecalho.index("PREÇO REAL") if "PREÇO REAL" in cabecalho else 4
                idx_img = cabecalho.index("URL_IMG") if "URL_IMG" in cabecalho else 6
                
                for linha in linhas[1:]:
                    # Ignora linhas em branco ou registros com colunas faltantes essenciais
                    if not linha or len(linha) <= max(idx_id, idx_categoria):
                        continue
                    
                    # Garante que não vai quebrar se a linha não tiver dados até o fim do preenchimento
                    while len(linha) < len(cabecalho):
                        linha.append("")
                        
                    # Só adiciona o produto se houver um link cadastrado na linha
                    link_afiliado = linha[idx_link].strip() if idx_link < len(linha) else ""
                    if not link_afiliado or link_afiliado == "":
                        continue
                    
                    produto = {
                        "id": linha[idx_id].strip() if idx_id < len(linha) else "",
                        "categoria": linha[idx_categoria].strip().upper() if idx_categoria < len(linha) else "",
                        "link_afiliado": link_afiliado,
                        "preco_atual": linha[idx_promo].strip() if idx_promo < len(linha) else "0.00",
                        "preco_antigo": linha[idx_real].strip() if idx_real < len(linha) else "",
                        "url_imagem": linha[idx_img].strip() if idx_img < len(linha) else ""
                    }
                    produtos_consolidados.append(produto)
                    
        except Exception as e:
            print(f"⚠️ Não foi possível ler a aba {nome_aba}: {e}")
            continue

    # Salva todos os produtos encontrados de todas as abas no arquivo JSON do site
    if produtos_consolidados:
        try:
            with open("produtos.json", "w", encoding="utf-8") as f:
                json.dump(produtos_consolidados, f, ensure_ascii=False, indent=2)
            print(f"\n✅ SUCESSO! O arquivo produtos.json foi gerado com {len(produtos_consolidados)} produtos de todas as abas!")
        except Exception as e:
            print(f"❌ Erro ao gravar o arquivo de produtos: {e}")
    else:
        print("\n⚠️ Nenhum produto válido com link de afiliado foi encontrado em nenhuma das abas.")

if __name__ == "__main__":
    baixar_dados_planilha()
