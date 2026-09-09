import os
import json
import urllib.request
import urllib.parse
import re
import time

# CONFIGURAÇÕES DA SUA AUTOMAÇÃO
CHAVE_API = "AIzaSyCOw0sef-Alux79-MuoQtH6oM525GVOC6g" # COLOQUE SUA CHAVE DE API QUE COMEÇA COM AIzaSy
LINK_OU_ID_PLANILHA = "https://docs.google.com/spreadsheets/d/1l_-h10C6XhYJ7wlM0MIOHVY0HjlXF8gPmNfSmiGDVsA/edit?usp=sharing" # COLOQUE O LINK COMPLETO DA SUA PLANILHA
NOME_ABA = "Página1"

def extrair_id_valido(valor):
    if "docs.google.com" in valor:
        match = re.search(r'/d/([a-zA-Z0-9-_]+)', valor)
        if match:
            return match.group(1).strip()
    return valor.strip()

def baixar_dados_planilha():
    # RESOLUÇÃO DO ERRO DE DNS: Força o ambiente Linux a limpar o cache de rede antigo
    os.environ['http_proxy'] = ''
    os.environ['https_proxy'] = ''
    
    id_planilha_limpo = extrair_id_valido(LINK_OU_ID_PLANILHA)
    chave_limpa = CHAVE_API.strip()
    aba_codificada = urllib.parse.quote(NOME_ABA.strip())
    
    url = f"https://googleapis.com{id_planilha_limpo}/values/{aba_codificada}?key={chave_limpa}"
    
    # Sistema de tentativas para driblar a queda de sinal do terminal
    tentativas = 3
    for tentativa in range(tentativas):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=15) as response:
                dados = json.loads(response.read().decode('utf-8'))
                linhas = dados.get('values', [])
                
                if not linhas or len(linhas) <= 1:
                    print("Planilha conectada, mas vazia ou sem dados abaixo do cabeçalho.")
                    return
                
                colunas_cabecalho = linhas
                produtos_lista = []
                
                for index, linha in enumerate(linhas[1:]):
                    while len(linha) < len(colunas_cabecalho):
                        linha.append("")
                    
                    produto = {
                        "id": str(index + 1),
                        "nome": linha[0] if len(linha) > 0 and linha[0] else "Produto Sem Nome",
                        "preco_atual": linha[1] if len(linha) > 1 and linha[1] else "0.00",
                        "preco_antigo": linha[2] if len(linha) > 2 and linha[2] else "",
                        "link_afiliado": linha[3] if len(linha) > 3 and linha[3] else "#",
                        "url_imagem": linha[4] if len(linha) > 4 and linha[4] else ""
                    }
                    produtos_lista.append(produto)
                
                with open("produtos.json", "w", encoding="utf-8") as f:
                    json.dump(produtos_lista, f, ensure_ascii=False, indent=2)
                print("\n✅ SUCESSO! O arquivo produtos.json foi gerado com os seus produtos!")
                return # Sai do programa após o sucesso
                
        except Exception as e:
            print(f"⚠️ Tentativa {tentativa + 1} falhou devido a oscilação de rede: {e}")
            if tentativa < tentativas - 1:
                time.sleep(3) # Aguarda 3 segundos antes de tentar reconectar
            else:
                print("\n❌ Erro crítico permanente: Não foi possível conectar ao servidor do Google Sheets. Verifique sua conexão ou se a planilha está marcada como pública.")

if __name__ == "__main__":
    baixar_dados_planilha()
