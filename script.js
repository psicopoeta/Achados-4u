document.addEventListener("DOMContentLoaded", () => {
    carregarVitrineTerapeutica();
});

async function carregarVitrineTerapeutica() {
    const subContainers = {
        // Bloco Regulação Sensorial
        "MORDEDORES": document.getElementById("container-mordedores"),
        "SPINNERS": document.getElementById("container-spinners"),
        "ABAFADOR": document.getElementById("container-abafador"),
        "WIDGETS/FIDGETS": document.getElementById("container-fidgets"),
        "SQUISHY/BOLINHAS": document.getElementById("container-squishy"),
        "TÁTIL/SENSORIAL": document.getElementById("container-tatil"),
        "TATIL/SENSORIAL": document.getElementById("container-tatil"),
        
        // Bloco Propriocepção e Vestibular
        "EQUILÍBRIO": document.getElementById("container-equilibrio"),
        "EQUILIBRIO": document.getElementById("container-equilibrio"),
        "BALANÇO": document.getElementById("container-balanco"),
        "BALANCO": document.getElementById("container-balanco"),
        "BOLAS": document.getElementById("container-bolas"),
        "MANTA/COLETE PONDERADO": document.getElementById("container-ponderado"),
        "TENSORES": document.getElementById("container-tensores"),
        
        // Outros Blocos Macros
        "PEDAGOGICO": document.getElementById("container-pedagogico"),
        "COGNITIVO": document.getElementById("container-pedagogico"),
        "POSTURA": document.getElementById("container-postura"),
        "MOTRICIDADE": document.getElementById("container-postura")
    };

    try {
        const response = await fetch("produtos.json");
        const produtos = await response.json();

        // Limpa visualmente as grades antes de injetar os itens
        Object.values(subContainers).forEach(grid => {
            if (grid) grid.innerHTML = "";
        });

        // Mostra uma mensagem de "Em breve" nas categorias vazias
        Object.entries(subContainers).forEach(([chave, grid]) => {
            if (grid && grid.children.length === 0) {
                grid.innerHTML = `<p class="aviso-vazio" style="color: #999; font-style: italic; padding: 10px;">Novos achadinhos sendo selecionados na planilha... ⏳</p>`;
            }
        });

        produtos.forEach(produto => {
            if (!produto.categoria) return;

            const categoriaChave = produto.categoria.trim().toUpperCase();
            const gridDestino = subContainers[categoriaChave];

            if (gridDestino) {
                // Se a mensagem de "Em breve" estiver lá, limpa antes do primeiro produto entrar
                if (gridDestino.querySelector(".aviso-vazio")) {
                    gridDestino.innerHTML = "";
                }

                const card = document.createElement("div");
                card.className = "card-produto"; // Puxa seu estilo do style.css

                const imagemUrl = produto.url_imagem && produto.url_imagem.startsWith("http")
                    ? produto.url_imagem 
                    : "https://placeholder.com";

                card.innerHTML = `
                    <div class="img-container">
                        <img src="${imagemUrl}" alt="${produto.nome}" style="max-width:100%; border-radius:8px; display:block; margin:0 auto;">
                    </div>
                    <h4 style="margin: 10px 0; font-size: 1.1em; color: #333;">${produto.nome}</h4>
                    <div class="precos" style="margin: 8px 0;">
                        ${produto.preco_antigo ? `<span class="preco-antigo" style="text-decoration:line-through; color:#999; font-size:0.9em; margin-right:8px;">R$ ${produto.preco_antigo}</span>` : ""}
                        <strong class="preco-atual" style="color:#2ecc71; font-size:1.2em;">R$ ${produto.preco_atual}</strong>
                    </div>
                    <a href="${produto.link_afiliado}" target="_blank" class="btn-comprar" style="display:block; text-align:center; padding:10px; background:#00a650; color:#fff; text-decoration:none; border-radius:6px; font-weight:bold; margin-top:10px;">Ver no Mercado Livre</a>
                `;
                gridDestino.appendChild(card);
            }
        });

    } catch (error) {
        console.error("Erro no carregamento visual da vitrine:", error);
    }
}

