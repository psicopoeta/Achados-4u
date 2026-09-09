document.addEventListener("DOMContentLoaded", () => {
    carregarProdutos();
});

async function carregarProdutos() {
    const container = document.getElementById("produtos-container"); // Garanta que seu HTML tem essa ID
    if (!container) return;

    try {
        // Busca o arquivo JSON atualizado automaticamente pela planilha
        const response = await fetch("produtos.json");
        const produtos = await response.json();

        container.innerHTML = ""; // Limpa itens antigos da tela

        produtos.forEach(produto => {
            const card = document.createElement("div");
            card.className = "card-produto"; // Usa suas classes do style.css

            card.innerHTML = `
                <div class="img-container">
                    <img src="${produto.url_imagem || 'img/placeholder.png'}" alt="${produto.nome}">
                </div>
                <h3>${produto.nome}</h3>
                ${produto.preco_antigo ? `<span class="preco-antigo">R$ ${produto.preco_antigo}</span>` : ''}
                <div class="preco-atual">R$ ${produto.preco_atual}</div>
                <a href="${produto.link_afiliado}" target="_blank" class="btn-comprar">Ver no Mercado Livre</a>
            `;
            container.appendChild(card);
        });
    } catch (error) {
        console.error("Erro ao carregar a vitrine de produtos:", error);
    }
}
