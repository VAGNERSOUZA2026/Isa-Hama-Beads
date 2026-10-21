import streamlit as st
import json
import os
import base64
import urllib.parse
from html import escape

st.set_page_config(page_title="Isa Hama Beads", page_icon="🌸", layout="wide", initial_sidebar_state="collapsed")

DATA_FILE = "produtos.json"
PHONE_WA = "5531989684010"
LOGO_FILE = "logo.png"

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Nunito:wght@500;600;700;800;900&display=swap');
:root{--pink:#f21887;--pink2:#ff5bad;--pink-pale:#ffe8f4;--purple:#7a39a6;--purple-pale:#f1e4ff;--ink:#292238;--muted:#796d80;--line:#f4d3e6;--white:#fff}
.stApp{background:linear-gradient(180deg,#fff5fb 0%,#fff 44%,#fff8fc 100%);color:var(--ink);font-family:'DM Sans',sans-serif}
.block-container{max-width:1120px;padding-top:1rem;padding-bottom:5rem}
[data-testid="stHeader"]{background:rgba(255,245,251,.92)}
h1,h2,h3{font-family:'Nunito',sans-serif;color:var(--ink);font-weight:900;letter-spacing:-.035em}
h1{font-size:clamp(2rem,5vw,3.2rem)!important;line-height:1.02}
h2{font-size:clamp(1.45rem,3vw,2rem)!important}
p,div,label{font-family:'DM Sans',sans-serif}
.stButton>button,.stFormSubmitButton>button,.stLinkButton>a{border:0;border-radius:999px;padding:.68rem 1rem;font-weight:800;color:white;background:linear-gradient(110deg,var(--pink),var(--pink2));box-shadow:0 7px 18px #f2188725;transition:transform .18s,box-shadow .18s}
.stButton>button:hover,.stFormSubmitButton>button:hover,.stLinkButton>a:hover{color:white;transform:translateY(-2px);box-shadow:0 10px 24px #f2188740}
.stTextInput input,.stTextArea textarea,.stNumberInput input,.stSelectbox div[data-baseweb="select"]{border-radius:13px;border-color:#edc6dd}
div[data-testid="stVerticalBlockBorderWrapper"]{border:1px solid var(--line);border-radius:22px;background:white;box-shadow:0 8px 24px #512b570a}
div[data-testid="stForm"]{border:1px solid var(--line);border-radius:20px;padding:18px;background:white}
div[data-testid="stExpander"]{border:1px solid var(--line);border-radius:18px;background:#fffafd}
div[data-testid="stImage"] img{border-radius:18px}
.brandbar{display:flex;align-items:center;gap:13px;background:#fff;border:1px solid var(--line);border-radius:22px;padding:12px 18px;margin-bottom:14px;box-shadow:0 8px 25px #5a23420b}
.brandname{font-family:'Nunito',sans-serif;font-size:1.4rem;font-weight:900;color:#52275e;line-height:1.1}
.brandtag{font-size:.82rem;color:var(--muted);margin-top:3px}
.hero{position:relative;overflow:hidden;border-radius:28px;padding:clamp(22px,4vw,40px);background:linear-gradient(135deg,#ffd9ec 0%,#f6e4ff 56%,#fff0d9 100%);border:1px solid #f6cde3;box-shadow:0 16px 40px #8a3b7014;margin:10px 0 24px}
.hero-kicker{display:inline-block;background:#fff;color:#c21c77;border:1px solid #f4b8d8;border-radius:999px;padding:7px 12px;font-size:.76rem;font-weight:900;letter-spacing:.04em}
.hero-copy{font-size:1rem;color:#69546e;line-height:1.65;max-width:560px}
.section-label{font-size:.78rem;font-weight:900;letter-spacing:.13em;color:#c02b7b;text-transform:uppercase}
.price{font-size:1.18rem;font-weight:900;color:#cf1878}
.muted{font-size:.86rem;color:var(--muted)}
.product-title{font-size:1.03rem;font-weight:900;color:#31253c;margin-top:7px}
.tag{display:inline-block;background:#fff0f8;border:1px solid #f6d0e4;border-radius:999px;color:#b91b73;padding:5px 10px;font-size:.75rem;font-weight:800}
.info-card{border:1px solid var(--line);background:white;border-radius:20px;padding:18px}
.empty{border:1px dashed #e9b9d5;border-radius:20px;background:#fffafd;padding:25px;text-align:center;color:#76637c}
div[data-testid="stRadio"] label{background:#fff;border:1px solid var(--line);padding:9px 12px;border-radius:14px}
[data-testid="stSidebar"]{background:#fff3fa}
hr{border-color:#f3d6e8}
footer{visibility:hidden}
@media(max-width:700px){.block-container{padding-left:1rem;padding-right:1rem;padding-top:.5rem}.brandbar{padding:10px 12px}.brandname{font-size:1.15rem}.hero{border-radius:22px;padding:22px}.hero-copy{font-size:.94rem}}
</style>
""", unsafe_allow_html=True)

def carregar_produtos():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
        except (json.JSONDecodeError, OSError):
            pass
    data = [
        {"id": 1, "nome": "Chaveiro colorido", "categoria": "Chaveiros", "preco": 8.0, "tamanho": "5 cm", "estoque": 10, "imagem": "", "descricao": "Chaveiro artesanal feito com Hama Beads."},
        {"id": 2, "nome": "Personagem personalizado", "categoria": "Personagens", "preco": 8.0, "tamanho": "5 cm", "estoque": 5, "imagem": "", "descricao": "Peça artesanal colorida. Consulte modelos disponíveis."}
    ]
    salvar_produtos(data)
    return data

def salvar_produtos(produtos):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(produtos, f, ensure_ascii=False, indent=2)

def imagem_data_url(upload):
    if not upload:
        return ""
    raw = upload.getvalue()
    mime = upload.type or "image/png"
    return "data:" + mime + ";base64," + base64.b64encode(raw).decode("ascii")

def mostrar_imagem(valor, width=None):
    if not valor:
        return False
    try:
        st.image(valor, width=width, use_container_width=(width is None))
        return True
    except Exception:
        return False

def navegar(pagina):
    st.session_state.pagina = pagina

def adicionar_carrinho(prod):
    carrinho = st.session_state.carrinho
    encontrado = next((item for item in carrinho if item["id"] == prod["id"]), None)
    if encontrado:
        encontrado["qtd"] += 1
    else:
        carrinho.append({"id": prod["id"], "nome": prod["nome"], "preco": float(prod.get("preco", 0)),
                         "tamanho": prod.get("tamanho", "5 cm"), "qtd": 1, "imagem": prod.get("imagem", "")})
    st.session_state.carrinho = carrinho
    st.toast("Adicionado à sacolinha!")

def preparar_pedido():
    carrinho = st.session_state.get("carrinho", [])
    nome = st.session_state.get("checkout_nome", "").strip()
    telefone = st.session_state.get("checkout_telefone", "").strip()
    entrega = st.session_state.get("checkout_entrega", "Retirar em mãos")
    endereco = st.session_state.get("checkout_endereco", "").strip()
    obs = st.session_state.get("checkout_observacoes", "").strip()
    if not carrinho:
        st.session_state.erro_pedido = "Sua sacolinha está vazia."
        return
    if not nome or not telefone:
        st.session_state.erro_pedido = "Preencha seu nome e telefone."
        return
    if entrega == "Receber por envio" and not endereco:
        st.session_state.erro_pedido = "Informe o CEP/cidade ou endereço para combinar o envio."
        return
    total = sum(float(i["preco"]) * int(i["qtd"]) for i in carrinho)
    linhas = ["Olá! Quero fazer este pedido na Isa Hama Beads:", ""]
    for i in carrinho:
        linhas.append(f"- {i['qtd']}x {i['nome']} ({i.get('tamanho','')}) — R$ {float(i['preco'])*int(i['qtd']):.2f}")
    linhas += ["", f"Total dos produtos: R$ {total:.2f}", f"Cliente: {nome}", f"Telefone: {telefone}", f"Entrega: {entrega}"]
    if endereco:
        linhas.append(f"Endereço/CEP: {endereco}")
    if obs:
        linhas.append(f"Observações: {obs}")
    st.session_state.url_pedido = "https://wa.me/" + PHONE_WA + "?text=" + urllib.parse.quote("\n".join(linhas))
    st.session_state.carrinho = []
    st.session_state.pedido_pronto = True
    st.session_state.erro_pedido = ""
    for key, value in {"checkout_nome": "", "checkout_telefone": "", "checkout_entrega": "Retirar em mãos",
                        "checkout_endereco": "", "checkout_observacoes": ""}.items():
        st.session_state[key] = value

produtos = carregar_produtos()
for key, value in {
    "pagina": "Início", "carrinho": [], "favoritos": [], "produto_selecionado": None,
    "pedido_pronto": False, "url_pedido": "", "erro_pedido": "", "mostrar_personalizacao": False
}.items():
    if key not in st.session_state:
        st.session_state[key] = value

# Header
h1, h2 = st.columns([1, 5], vertical_alignment="center")
with h1:
    if os.path.exists(LOGO_FILE):
        st.image(LOGO_FILE, width=86)
    else:
        st.markdown("## 🌸")
with h2:
    st.markdown("<div class='brandname'>Isa Hama Beads</div><div class='brandtag'>Chaveiros artesanais feitos com muito carinho 💗</div>", unsafe_allow_html=True)

# Navigation inspired by the reference
nav_items = ["Início", "Categorias", "Favoritos", f"Sacolinha ({sum(i['qtd'] for i in st.session_state.carrinho)})"]
nav_cols = st.columns(4)
for idx, label in enumerate(nav_items):
    page = label.split(" (")[0]
    with nav_cols[idx]:
        if st.button(("♡  " if page == "Favoritos" else "🛍  " if page == "Sacolinha" else "⌂  " if page == "Início" else "▦  ") + page,
                     key=f"nav_{idx}", use_container_width=True,
                     type="primary" if st.session_state.pagina == page else "secondary"):
            navegar(page)
            st.rerun()

st.markdown("<div style='height:3px;border-radius:8px;background:linear-gradient(90deg,#ff1688,#ff8ac7,#b77af2);margin:6px 0 20px'></div>", unsafe_allow_html=True)

pagina = st.session_state.pagina

if pagina == "Início":
    left, right = st.columns([1.25, 1], vertical_alignment="center")
    with left:
        st.markdown("""
        <section class="hero">
          <span class="hero-kicker">✦ FEITO À MÃO, COM CRIATIVIDADE</span>
          <h1 style="margin:.7rem 0;color:#4b285f">Pequenos detalhes que fazem grandes sorrisos! 💗</h1>
          <p class="hero-copy">Chaveiros coloridos feitos com Hama Beads. Encontre seu favorito ou peça uma criação exclusiva.</p>
        </section>
        """, unsafe_allow_html=True)
        if st.button("🌸 Explorar chaveiros", use_container_width=True):
            navegar("Categorias")
            st.rerun()
        if st.button("✨ Personalizar meu chaveiro", use_container_width=True):
            navegar("Personalizar")
            st.rerun()
    with right:
        if os.path.exists(LOGO_FILE):
            st.image(LOGO_FILE, use_container_width=True)
        else:
            st.markdown("<div class='hero' style='text-align:center;font-size:4rem'>🌸🧸✨</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-label'>Escolha seu estilo</div>", unsafe_allow_html=True)
    cats = sorted(set(str(p.get("categoria", "Chaveiros")) for p in produtos))
    cat_cols = st.columns(min(4, max(1, len(cats))))
    for idx, cat in enumerate(cats[:4]):
        with cat_cols[idx]:
            if st.button("🌷 " + cat, key=f"cat_home_{idx}", use_container_width=True):
                st.session_state.categoria_filtro = cat
                navegar("Categorias")
                st.rerun()

    st.markdown("## 💖 Destaques")
    destaques = [p for p in produtos if int(p.get("estoque", 0)) > 0][:4]
    if not destaques:
        st.markdown("<div class='empty'>Novos chaveiros estão chegando. Volte em breve! 🌸</div>", unsafe_allow_html=True)
    else:
        cols = st.columns(min(4, len(destaques)))
        for idx, prod in enumerate(destaques):
            with cols[idx]:
                if not mostrar_imagem(prod.get("imagem", "")):
                    st.markdown("<div style='background:linear-gradient(145deg,#ffe4f2,#f1e4ff);border-radius:18px;padding:28px 8px;text-align:center;font-size:3rem'>🧸💗</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='product-title'>{escape(str(prod['nome']))}</div><div class='price'>R$ {float(prod.get('preco',0)):.2f}</div>", unsafe_allow_html=True)
                if st.button("Ver detalhes", key=f"home_detail_{prod['id']}", use_container_width=True):
                    st.session_state.produto_selecionado = prod["id"]
                    navegar("Detalhes")
                    st.rerun()

elif pagina == "Categorias":
    st.markdown("<div class='section-label'>Feitos à mão, peça por peça</div>", unsafe_allow_html=True)
    st.title("Encontre seu chaveiro 💕")
    a, b = st.columns([2, 1])
    with a:
        busca = st.text_input("Buscar produtos", placeholder="Digite o nome do chaveiro...", key="busca_catalogo")
    with b:
        categorias = ["Todas"] + sorted(set(str(p.get("categoria", "Chaveiros")) for p in produtos))
        escolha = st.selectbox("Categoria", categorias, key="categoria_catalogo")
    filtrados = [p for p in produtos if busca.lower() in str(p.get("nome", "")).lower()]
    if escolha != "Todas":
        filtrados = [p for p in filtrados if p.get("categoria", "Chaveiros") == escolha]
    if not filtrados:
        st.markdown("<div class='empty'>Não encontramos chaveiros com esse filtro. Tente outra busca. 🌸</div>", unsafe_allow_html=True)
    else:
        cols = st.columns(3)
        for idx, prod in enumerate(filtrados):
            with cols[idx % 3]:
                with st.container(border=True):
                    if not mostrar_imagem(prod.get("imagem", "")):
                        st.markdown("<div style='background:linear-gradient(145deg,#ffe4f2,#f1e4ff);border-radius:18px;padding:34px 8px;text-align:center;font-size:3rem'>🧸🌸</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='tag'>{escape(str(prod.get('categoria','Chaveiros')))}</div><div class='product-title'>{escape(str(prod['nome']))}</div><div class='muted'>Tamanho aproximado: {escape(str(prod.get('tamanho','5 cm')))}</div><div class='price'>R$ {float(prod.get('preco',0)):.2f}</div>", unsafe_allow_html=True)
                    if int(prod.get("estoque", 0)) > 0:
                        c1, c2 = st.columns(2)
                        with c1:
                            if st.button("♡ Favoritar" if prod["id"] not in st.session_state.favoritos else "♥ Favorito",
                                         key=f"fav_{prod['id']}", use_container_width=True):
                                if prod["id"] in st.session_state.favoritos:
                                    st.session_state.favoritos.remove(prod["id"])
                                else:
                                    st.session_state.favoritos.append(prod["id"])
                                st.rerun()
                        with c2:
                            if st.button("Ver detalhes", key=f"detail_{prod['id']}", use_container_width=True):
                                st.session_state.produto_selecionado = prod["id"]
                                navegar("Detalhes")
                                st.rerun()
                        if st.button("＋ Adicionar à sacolinha", key=f"add_{prod['id']}", use_container_width=True):
                            adicionar_carrinho(prod)
                            st.rerun()
                    else:
                        st.button("Esgotado", key=f"out_{prod['id']}", disabled=True, use_container_width=True)

elif pagina == "Detalhes":
    prod = next((p for p in produtos if p["id"] == st.session_state.produto_selecionado), None)
    if not prod:
        st.info("Escolha um chaveiro no catálogo para ver os detalhes.")
        if st.button("Voltar ao catálogo"):
            navegar("Categorias")
            st.rerun()
    else:
        if st.button("← Voltar ao catálogo"):
            navegar("Categorias")
            st.rerun()
        pic, info = st.columns([1.15, 1], vertical_alignment="top")
        with pic:
            if not mostrar_imagem(prod.get("imagem", "")):
                st.markdown("<div style='background:linear-gradient(145deg,#ffe4f2,#f1e4ff);border-radius:24px;padding:90px 10px;text-align:center;font-size:5rem'>🧸💗</div>", unsafe_allow_html=True)
        with info:
            st.markdown(f"<div class='tag'>{escape(str(prod.get('categoria','Chaveiros')))}</div>", unsafe_allow_html=True)
            st.title(str(prod["nome"]))
            st.markdown(f"<div class='price' style='font-size:1.7rem'>R$ {float(prod.get('preco',0)):.2f}</div>", unsafe_allow_html=True)
            st.write(prod.get("descricao", "Chaveiro artesanal feito com Hama Beads."))
            st.write(f"**Tamanho:** {prod.get('tamanho','5 cm')}")
            st.write(f"**Disponibilidade:** {'Em estoque' if int(prod.get('estoque',0)) > 0 else 'Esgotado'}")
            if st.button("♡ Adicionar aos favoritos", use_container_width=True):
                if prod["id"] in st.session_state.favoritos:
                    st.session_state.favoritos.remove(prod["id"])
                else:
                    st.session_state.favoritos.append(prod["id"])
                st.rerun()
            if int(prod.get("estoque",0)) > 0 and st.button("🛍 Adicionar à sacolinha", use_container_width=True):
                adicionar_carrinho(prod)
                navegar("Sacolinha")
                st.rerun()

elif pagina == "Favoritos":
    st.title("Seus favoritos 💗")
    favoritos = [p for p in produtos if p["id"] in st.session_state.favoritos]
    if not favoritos:
        st.markdown("<div class='empty'>Você ainda não favoritou nenhum chaveiro. Explore o catálogo e toque no coração. ♡</div>", unsafe_allow_html=True)
        if st.button("Explorar catálogo"):
            navegar("Categorias")
            st.rerun()
    else:
        cols = st.columns(3)
        for idx, prod in enumerate(favoritos):
            with cols[idx % 3]:
                with st.container(border=True):
                    if not mostrar_imagem(prod.get("imagem", "")):
                        st.markdown("<div style='background:linear-gradient(145deg,#ffe4f2,#f1e4ff);border-radius:18px;padding:28px;text-align:center;font-size:3rem'>🌸💗</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='product-title'>{escape(str(prod['nome']))}</div><div class='price'>R$ {float(prod.get('preco',0)):.2f}</div>", unsafe_allow_html=True)
                    if st.button("Remover dos favoritos", key=f"unfav_{prod['id']}", use_container_width=True):
                        st.session_state.favoritos.remove(prod["id"])
                        st.rerun()
                    if st.button("Ver detalhes", key=f"favdetail_{prod['id']}", use_container_width=True):
                        st.session_state.produto_selecionado = prod["id"]
                        navegar("Detalhes")
                        st.rerun()

elif pagina == "Sacolinha":
    st.title("Minha sacolinha 🛍️")
    if not st.session_state.carrinho:
        st.markdown("<div class='empty'>Sua sacolinha está vazia.<br>Escolha um chaveiro para começar! 🌸</div>", unsafe_allow_html=True)
        if st.button("Continuar comprando", use_container_width=True):
            navegar("Categorias")
            st.rerun()
    else:
        total = 0.0
        for idx, item in enumerate(st.session_state.carrinho):
            subtotal = float(item["preco"]) * int(item["qtd"])
            total += subtotal
            with st.container(border=True):
                pcol, ncol, qcol, dcol = st.columns([1, 2.3, 1.2, .8], vertical_alignment="center")
                with pcol:
                    if not mostrar_imagem(item.get("imagem", "")):
                        st.markdown("🌸")
                with ncol:
                    st.markdown(f"**{escape(str(item['nome']))}**")
                    st.markdown(f"<span class='muted'>R$ {float(item['preco']):.2f} cada</span>", unsafe_allow_html=True)
                with qcol:
                    st.write(f"Qtd.: {item['qtd']}")
                    c1, c2 = st.columns(2)
                    with c1:
                        if st.button("−", key=f"menos_{idx}"):
                            item["qtd"] = max(1, int(item["qtd"])-1)
                            st.rerun()
                    with c2:
                        if st.button("+", key=f"mais_{idx}"):
                            item["qtd"] = int(item["qtd"])+1
                            st.rerun()
                with dcol:
                    if st.button("🗑", key=f"rem_{idx}"):
                        st.session_state.carrinho.pop(idx)
                        st.rerun()
        st.markdown(f"<div class='info-card'><div class='muted'>Subtotal dos produtos</div><div style='font-size:1.7rem;font-weight:900;color:#c91878'>R$ {total:.2f}</div><div class='muted'>Frete, se houver, será combinado pelo WhatsApp.</div></div>", unsafe_allow_html=True)
        st.markdown("## Finalizar pedido")
        with st.form("form_checkout"):
            st.text_input("Nome", placeholder="Como podemos chamar você?", key="checkout_nome")
            st.text_input("Telefone/WhatsApp", placeholder="DDD + número", key="checkout_telefone")
            st.radio("Como deseja receber?", ["Retirar em mãos", "Receber por envio"], horizontal=True, key="checkout_entrega")
            if st.session_state.get("checkout_entrega") == "Receber por envio":
                st.text_input("CEP, cidade e endereço", placeholder="Informe os dados para combinar o envio", key="checkout_endereco")
            st.text_area("Observações (opcional)", placeholder="Alguma informação para a loja?", key="checkout_observacoes")
            st.form_submit_button("📲 Preparar pedido no WhatsApp", on_click=preparar_pedido, use_container_width=True)
        if st.session_state.erro_pedido:
            st.error(st.session_state.erro_pedido)
        if st.session_state.pedido_pronto and st.session_state.url_pedido:
            st.success("Pedido preparado. A sacolinha foi esvaziada e os campos foram limpos.")
            st.link_button("Abrir WhatsApp e enviar pedido", st.session_state.url_pedido, use_container_width=True)
            if st.button("Concluir e fechar aviso"):
                st.session_state.pedido_pronto = False
                st.session_state.url_pedido = ""
                st.rerun()
        st.caption("O pedido só é enviado quando você abrir o WhatsApp e tocar em enviar. O pagamento será combinado diretamente com a loja.")

elif pagina == "Personalizar":
    st.title("Crie seu chaveiro personalizado ✨")
    st.write("Conte sua ideia. O orçamento será combinado pelo WhatsApp.")
    with st.form("form_personalizado", clear_on_submit=True):
        nome_personagem = st.text_input("Nome ou personagem desejado", placeholder="Ex.: meu gato, personagem, logo...")
        tamanho_opc = st.selectbox("Tamanho", ["5 cm", "7 cm", "10 cm", "Personalizado"])
        qtd_pers = st.number_input("Quantidade", min_value=1, value=1, step=1)
        cores_desejadas = st.text_input("Cores desejadas", placeholder="Ex.: rosa, branco e lilás")
        obs_modelo = st.text_area("Detalhes do modelo", placeholder="Descreva como gostaria do chaveiro")
        foto_ref = st.file_uploader("Foto de referência (opcional)", type=["png", "jpg", "jpeg"], key="foto_personalizado")
        enviar = st.form_submit_button("Pedir orçamento pelo WhatsApp", use_container_width=True)
    if enviar:
        mensagem = ("Olá! Quero um orçamento de chaveiro personalizado.\n"
                    f"Modelo: {nome_personagem or 'A combinar'}\nTamanho: {tamanho_opc}\nQuantidade: {qtd_pers}\n"
                    f"Cores: {cores_desejadas or 'A combinar'}\nDetalhes: {obs_modelo or 'Nenhum'}\n"
                    + ("Tenho uma foto de referência e vou anexá-la nesta conversa." if foto_ref else ""))
        st.success("O orçamento está pronto. Se tiver uma foto, anexe-a no WhatsApp.")
        st.link_button("Abrir WhatsApp", "https://wa.me/" + PHONE_WA + "?text=" + urllib.parse.quote(mensagem), use_container_width=True)
    if st.button("← Voltar ao início"):
        navegar("Início")
        st.rerun()

# Footer
st.markdown("---")
st.markdown("<div style='text-align:center;color:#8b758e;padding:10px'><b style='color:#b51f76'>Isa Hama Beads</b><br>Feito à mão, peça por peça 💗<br><small>Pedidos e informações pelo WhatsApp</small></div>", unsafe_allow_html=True)

# Admin
with st.expander("🔐 Acesso administrativo"):
    admin_password = st.secrets.get("ADMIN_PASSWORD", "")
    if not admin_password:
        st.warning("Configure ADMIN_PASSWORD em Settings → Secrets no Streamlit. Não deixe a senha no código porque o repositório é público.")
    senha = st.text_input("Senha do administrador", type="password", key="admin_password_input")
    if admin_password and senha == admin_password:
        st.success("Painel administrativo liberado.")
        st.markdown("### Cadastrar chaveiro")
        with st.form("novo_prod_adm", clear_on_submit=True):
            nome = st.text_input("Nome do chaveiro")
            categoria = st.text_input("Categoria", value="Personagens")
            preco = st.number_input("Preço (R$)", min_value=0.0, value=8.0, step=1.0)
            tamanho = st.text_input("Tamanho", value="5 cm")
            estoque = st.number_input("Estoque", min_value=0, value=5, step=1)
            descricao = st.text_area("Descrição", placeholder="Descrição do chaveiro")
            imagem_upload = st.file_uploader("Imagem do chaveiro", type=["png", "jpg", "jpeg"], key="imagem_novo_prod")
            salvar = st.form_submit_button("Cadastrar produto", use_container_width=True)
        if salvar:
            if not nome.strip():
                st.error("Informe o nome do produto.")
            else:
                novo_id = max([int(p.get("id",0)) for p in produtos], default=0) + 1
                produtos.append({"id": novo_id, "nome": nome.strip(), "categoria": categoria.strip() or "Chaveiros",
                                 "preco": float(preco), "tamanho": tamanho.strip(), "estoque": int(estoque),
                                 "descricao": descricao.strip(), "imagem": imagem_data_url(imagem_upload)})
                salvar_produtos(produtos)
                st.success("Chaveiro cadastrado.")
                st.rerun()
        st.markdown("### Produtos cadastrados")
        for p in produtos:
            with st.container(border=True):
                pc1, pc2 = st.columns([3, 1])
                with pc1:
                    st.write(f"**{p['nome']}** · R$ {float(p['preco']):.2f} · Estoque: {p['estoque']}")
                    mostrar_imagem(p.get("imagem", ""), width=120)
                with pc2:
                    if st.button("Excluir", key=f"excluir_{p['id']}"):
                        produtos = [x for x in produtos if x["id"] != p["id"]]
                        salvar_produtos(produtos)
                        st.rerun()
    elif senha:
        st.error("Senha incorreta.")
