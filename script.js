document.addEventListener("DOMContentLoaded", () => {
    configurarMenuCategorias();
    carregarVitrineTerapeutica();
});

/* ============ MENU DROPDOWN DE CATEGORIAS ============ */
function configurarMenuCategorias() {
    const toggle = document.querySelector(".dropdown-toggle");
    const menu = document.querySelector(".dropdown-menu");
    if (!toggle || !menu) return;

    toggle.addEventListener("click", (e) => {
        e.preventDefault();
        const aberto = menu.classList.toggle("active");
        toggle.setAttribute("aria-expanded", aberto);
    });

    // Fecha ao clicar fora do menu
    document.addEventListener("click", (e) => {
        if (!e.target.closest(".dropdown")) {
            menu.classList.remove("active");
            toggle.setAttribute("aria-expanded", "false");
        }
    });

    // Fecha após clicar numa categoria (navegação por âncora)
    menu.querySelectorAll("a").forEach((link) => {
        link.addEventListener("click", () => {
            menu.classList.remove("active");
            toggle.setAttribute("aria-expanded", "false");
        });
    });
}

/* ============ VITRINE DE PRODUTOS ============ */
function normalizar(txt) {
    return (txt || "")
        .trim()
        .toUpperCase()
        .normalize("NFD")
        .replace(/[̀-ͯ]/g, "");
}

// Categoria da planilha → ID da div no HTML (aceita variações de nome)
const MAPA_CATEGORIAS = {
    "MORDEDOR": "sub-mordedores",
    "MORDEDORES": "sub-mordedores",
    "SPINNER": "sub-spinners",
    "SPINNERS": "sub-spinners",
    "ABAFADOR": "sub-abafador",
    "ABAFADORES": "sub-abafador",
    "WIDGETS/FIDGETS": "sub-fidgets",
    "WIDGET": "sub-fidgets",
    "SQUISHY/BOLINHAS": "sub-squishy",
    "SQUISHY": "sub-squishy",
    "TATIL SENSORIAL": "sub-tatil",
    "TATIL/SENSORIAL": "sub-tatil",
    "EQUILIBRIO": "sub-equilibrio",
    "BALANCO": "sub-balanco",
    "BOLAS": "sub-bolas",
    "MANTA/COLETE PONDERADO": "sub-ponderado",
    "MANTA PONDERADA": "sub-ponderado",
    "COLETE PONDERADO": "sub-ponderado",
    "TENSORES": "sub-tensores",
    "PEDAGOGICO": "sub-pedagogico",
    "COGNITIVO": "sub-pedagogico",
    "PEDAGOGICO E COGNITIVO": "sub-pedagogico",
    "POSTURA": "sub-postura",
    "MOTRICIDADE": "sub-postura",
    "POSTURA E MOTRICIDADE": "sub-postura"
};

function fmtPreco(valor) {
    const v = (valor || "").toString().trim();
    if (!v) return "";
    return v.startsWith("R$") ? v : `R$ ${v}`;
}

async function carregarVitrineTerapeutica() {
    // Mensagem inicial em todas as grades
    document.querySelectorAll(".grade-produtos").forEach((g) => {
        g.innerHTML = `<p class="aviso-vazio" style="color:#999; font-style:italic; padding:10px;">Novos achadinhos sendo selecionados na planilha... ⏳</p>`;
    });

    let produtos = [];
    try {
        const response = await fetch("produtos.json");
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        produtos = await response.json();
    } catch (error) {
        console.error("Erro ao carregar produtos.json:", error);
        return;
    }

    produtos.forEach((produto) => {
        const link = (produto.link_afiliado || "").trim();

        // Ignora linhas de cabeçalho repetidas e linhas sem link real
        if (!/^https?:\/\//i.test(link)) return;
        if (["ID", "URL_LINK_PROD"].includes(normalizar(produto.id))) return;

        const destinoId = MAPA_CATEGORIAS[normalizar(produto.categoria)];
        if (!destinoId) return;

        const grid = document.getElementById(destinoId);
        if (!grid) return;

        const aviso = grid.querySelector(".aviso-vazio");
        if (aviso) aviso.remove();

        const nome = (produto.nome || "").trim() || "Produto em destaque";
        const precoAtual = fmtPreco(produto.preco_atual);
        const precoAntigo = fmtPreco(produto.preco_antigo);
        const imgUrl = (produto.url_imagem || "").trim();

        const blocoImg = /^https?:\/\//i.test(imgUrl)
            ? `<div class="img-container"><img src="${imgUrl}" alt="${nome}" style="max-width:100%; border-radius:8px; display:block; margin:0 auto;"></div>`
            : `<div class="img-container" style="min-height:120px; display:flex; align-items:center; justify-content:center; background:#eee; border-radius:8px; color:#999;">📷 imagem em breve</div>`;

        const blocoAntigo = (precoAntigo && precoAntigo !== precoAtual)
            ? `<span class="preco-antigo" style="text-decoration:line-through; color:#999; font-size:0.9em; margin-right:8px;">${precoAntigo}</span>`
            : "";

        const card = document.createElement("div");
        card.className = "card-produto";
        card.innerHTML = `
            ${blocoImg}
            <h4 style="margin:10px 0; font-size:1.1em; color:#333;">${nome}</h4>
            <div class="precos" style="margin:8px 0;">
                ${blocoAntigo}
                <strong class="preco-atual" style="color:#2ecc71; font-size:1.2em;">${precoAtual}</strong>
            </div>
            <a href="${link}" target="_blank" rel="noopener" class="btn-comprar" style="display:block; text-align:center; padding:10px; background:#00a650; color:#fff; text-decoration:none; border-radius:6px; font-weight:bold; margin-top:10px;">Ver no Mercado Livre</a>
        `;
        grid.appendChild(card);
    });
}

