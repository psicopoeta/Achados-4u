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
    "FAIXAS COMPRESSÃO": "sub-faixas",
    "PROTETOR DE CABEÇA": "sub-protetor",
    "PEDAGOGICO": "sub-pedagogico",
    "MEMORIA": "sub-memoria",
    "COMUNICAÇÃO / FALA / LEITURA": "sub-comunicacao",
    "JOGO PEDAGOGICO": "sub-jogo",
    "QUEBRACABEÇA": "sub-quebracabeça",
    "LOUSA": "sub-lousa",
    "COGNITIVO": "sub-pedagogico",
    "PEDAGOGICO E COGNITIVO": "sub-pedagogico",
    "POSTURA": "sub-postura",
    "MOTRICIDADE": "sub-motricidade",
    "POSTURA E MOTRICIDADE": "sub-postura"
};

// Removemos a antiga função fmtPreco e criamos um validador de tags comerciais
function obterTextoComercial(valor, tipo) {
    const v = (valor || "").toString().trim();
    if (!v) {
        // Se a planilha estiver vazia, define um texto padrão inteligente
        return tipo === "atual" ? "🔥 Ver Preço Promocional" : "OFERTA ATIVA";
    }
    // Se você escreveu algo na planilha (ex: "Frete Grátis"), mantém o texto puro
    return v;
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
        
        // Puxa o texto comercial da planilha ou aplica o padrão caso esteja vazio
        const textoAtual = obterTextoComercial(produto.preco_atual, "atual");
        const textoAntigo = obterTextoComercial(produto.preco_antigo, "antigo");
        const imgUrl = (produto.url_imagem || "").trim();

        const blocoImg = /^https?:\/\//i.test(imgUrl)
            ? `<div class="img-container"><img src="${imgUrl}" alt="${nome}" style="max-width:100%; border-radius:8px; display:block; margin:0 auto;"></div>`
            : `<div class="img-container" style="min-height:120px; display:flex; align-items:center; justify-content:center; background:#eee; border-radius:8px; color:#999;">📷 imagem em breve</div>`;

        // Renderiza a tag de destaque antiga apenas se fizer sentido
        const blocoAntigo = (textoAntigo && textoAntigo !== textoAtual)
            ? `<span class="tag-oferta" style="background:#ffeaa7; color:#d63031; font-size:0.8em; padding:2px 6px; border-radius:4px; font-weight:bold; margin-right:8px; text-transform:uppercase;">${textoAntigo}</span>`
            : "";

        const card = document.createElement("div");
        card.className = "card-produto";
        card.innerHTML = `
            ${blocoImg}
            <h4 style="margin:10px 0; font-size:1.1em; color:#333;">${nome}</h4>
            <div class="precos" style="margin:8px 0; display:flex; align-items:center; min-height:28px;">
                ${blocoAntigo}
                <strong class="preco-atual" style="color:#2ecc71; font-size:1.1em;">${textoAtual}</strong>
            </div>
            <a href="${link}" target="_blank" rel="noopener" class="btn-comprar" style="display:block; text-align:center; padding:10px; background:#00a650; color:#fff; text-decoration:none; border-radius:6px; font-weight:bold; margin-top:10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">Ver no Mercado Livre</a>
        `;
        grid.appendChild(card);
    });
}

