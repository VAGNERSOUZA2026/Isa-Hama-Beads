import streamlit as st
import json
import os
import base64
import urllib.parse
import requests
from html import escape

st.set_page_config(page_title="Isa Hama Beads | Chaveiros artesanais", page_icon="🌸", layout="wide")

DATA_FILE = "produtos.json"
PHONE_WA = "5531989684010"
LOGO_FILE = "logo.png"

# Paleta moderna inspirada em Hama Beads
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');
:root { --pink:#e84d9b; --purple:#7545a8; --ink:#30243a; --cream:#fff8fc; }
.stApp { background: linear-gradient(180deg,#fff8fc 0%,#fff 42%,#fff8fc 100%); color:var(--ink); }
.block-container { max-width: 1180px; padding-top: 1.4rem; }
h1,h2,h3 { color:#4b285f; font-family:'Playfair Display',serif; }
p,div,label { font-family:'DM Sans',sans-serif; }
.stButton>button, .stFormSubmitButton>button {
  border:0; border-radius:14px; padding:.68rem 1rem; font-weight:700;
  color:white; background:linear-gradient(115deg,#e84d9b,#8750bb);
  box-shadow:0 7px 18px #d85b9b26; transition:transform .2s, box-shadow .2s;
}
.stButton>button:hover,.stFormSubmitButton>button:hover { color:white; transform:translateY(-2px); box-shadow:0 10px 24px #d85b9b3d; }
div[data-testid="stMetric"], div[data-testid="stVerticalBlockBorderWrapper"] {
  border:1px solid #f5d8e9; border-radius:18px; background:#fff; padding:12px;
}
.hero {
  position:relative; overflow:hidden; border-radius:28px; padding:28px 30px;
  background:linear-gradient(125deg,#fff0f8 0%,#f4eaff 50%,#fff8e9 100%);
  border:1px solid #f4d9ea; box-shadow:0 15px 45px #6d3a7c12; margin-bottom:22px;
}
.hero:after { content:""; position:absolute; width:220px;height:220px;border-radius:50%;
  right:-55px;top:-75px;background:radial-gradient(circle,#e84d9b30,transparent 68%); }
.hero-title { font-family:'Playfair Display',serif; color:#4b285f; font-size:clamp(2rem,4vw,3.2rem); line-height:1.08; margin:.4rem 0; }
.hero-sub { color:#6d5b76; font-size:1.04rem; max-width:620px; }
.pill { display:inline-block; padding:6px 12px; border-radius:999px; background:#fff; color:#a52d77; font-weight:700; font-size:.8rem; border:1px solid #f2cce1; }
.product-card { border:1px solid #f1dce9; border-radius:20px; background:white; padding:14px; box-shadow:0 8px 22px #4b285f0a; }
.price { color:#9b2f7b; font-size:1.25rem; font-weight:800; }
.small-muted { color:#82738a; font-size:.88rem; }
@keyframes floatLogo { 0%,100%{transform:translateY(0) rotate(-1deg)} 50%{transform:translateY(-8px) rotate(1deg)} }
.floating-logo { animation:floatLogo 4s ease-in-out infinite; }
@keyframes shimmer { 0%{background-position:0% 50%} 100%{background-position:200% 50%} }
.animated-strip { height:5px;border-radius:20px;background:linear-gradient(90deg,#e84d9b,#8e58bd,#f5b7d8,#e84d9b);background-size:200% 100%;animation:shimmer 5s linear infinite;margin:10px 0 22px; }
footer { visibility:hidden; }
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
        {"id": 1, "nome": "Homem-Aranha", "categoria": "Personagens", "preco": 8.0, "tamanho": "5 cm", "estoque": 10, "imagem": ""},
        {"id": 2, "nome": "Sprunki", "categoria": "Personagens", "preco": 8.0, "tamanho": "5 cm", "estoque": 5, "imagem": ""}
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
        if valor.startswith("data:image/"):
            st.image(valor, width=width, use_container_width=(width is None))
        elif valor.startswith("http://") or valor.startswith("https://"):
            st.image(valor, width=width, use_container_width=(width is None))
        else:
            st.image(valor, width=width, use_container_width=(width is None))
        return True
    except Exception:
        return False

produtos = carregar_produtos()
if "carrinho" not in st.session_state:
    st.session_state.carrinho = []
if "ver_carrinho" not in st.session_state:
    st.session_state.ver_carrinho = False

# Cabeçalho com logo ampliada
top1, top2 = st.columns([1, 4], vertical_alignment="center")
with top1:
    if os.path.exists(LOGO_FILE):
        st.image(LOGO_FILE, width=220)
    else:
        st.markdown("<div style='font-size:3.6rem;text-align:center'>🌸🧵</div>", unsafe_allow_html=True)
with top2:
    st.markdown("<div class='pill'>✦ FEITO À MÃO, COM CRIATIVIDADE</div><h1 style='margin:.25rem 0'>Isa Hama Beads</h1><div class='small-muted'>Chaveiros artesanais coloridos, personalizados e cheios de personalidade.</div>", unsafe_allow_html=True)
st.markdown("<div class='animated-strip'></div>", unsafe_allow_html=True)

# Hero / logo animada em estilo de apresentação
hero_left, hero_right = st.columns([1.6, 1], vertical_alignment="center")
with hero_left:
    st.markdown("""
    <section class="hero">
      <span class="pill">🌈 Seu estilo em pequenas peças</span>
      <div class="hero-title">Pequenos detalhes.<br>Grandes ideias.</div>
      <p class="hero-sub">Escolha seu chaveiro favorito ou peça uma criação exclusiva feita com Hama Beads.</p>
      <p style="color:#7545a8;font-weight:700">💗 Presentes criativos • Personagens • Modelos personalizados</p>
    </section>
    """, unsafe_allow_html=True)
with hero_right:
    if os.path.exists(LOGO_FILE):
        st.markdown("<div class='floating-logo'>", unsafe_allow_html=True)
        st.image(LOGO_FILE, width=300)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='hero' style='text-align:center;font-size:5rem'>🧸🌸✨<p style='font-size:1rem'>Criatividade em cada miçanga</p></div>", unsafe_allow_html=True)

# Contact / custom order
st.markdown("## ✨ Crie seu chaveiro personalizado")
st.markdown("Conte sua ideia e envie a referência pelo WhatsApp. O valor é combinado após avaliar o modelo.")
with st.form("form_personalizado"):
    foto_ref = st.file_uploader("Foto de referência (opcional)", type=["png", "jpg", "jpeg"], key="foto_ref")
    nome_personagem = st.text_input("Nome ou personagem desejado", placeholder="Ex.: meu gato, personagem, logo...")
    a, b = st.columns(2)
    with a:
        tamanho_opc = st.selectbox("Tamanho", ["5 cm", "7 cm", "10 cm", "Personalizado"])
    with b:
        qtd_pers = st.number_input("Quantidade", min_value=1, value=1, step=1)
    cores_desejadas = st.text_input("Cores desejadas", placeholder="Ex.: rosa, branco e dourado")
    obs_modelo = st.text_area("Detalhes do modelo", placeholder="Texto, acabamento ou outras preferências")
    enviar_orcamento = st.form_submit_button("📲 Pedir orçamento pelo WhatsApp", use_container_width=True)
if enviar_orcamento:
    mensagem = ("Olá! Gostaria de um orçamento para chaveiro personalizado:\n"
                f"Nome/personagem: {nome_personagem or 'A combinar'}\nTamanho: {tamanho_opc}\nQuantidade: {qtd_pers}\n"
                f"Cores: {cores_desejadas or 'A combinar'}\nObservações: {obs_modelo or 'Nenhuma'}\n"
                + ("Tenho uma imagem de referência e vou anexá-la nesta conversa." if foto_ref else "Ainda não tenho imagem de referência."))
    st.success("Abra o WhatsApp e envie a mensagem. Se tiver uma foto, anexe-a na conversa.")
    st.link_button("Abrir WhatsApp", f"https://wa.me/{PHONE_WA}?text={urllib.parse.quote(mensagem)}", use_container_width=True)

st.markdown("---")

# Cart panel
st.markdown("## 🛍️ Sua sacolinha")
st.session_state.ver_carrinho = st.toggle("Mostrar carrinho", value=st.session_state.ver_carrinho)
if st.session_state.ver_carrinho:
    if not st.session_state.carrinho:
        st.info("Sua sacolinha está vazia. Adicione um chaveiro do catálogo.")
    else:
        total_pedido = 0.0
        for idx, item in enumerate(st.session_state.carrinho):
            subtotal = float(item["preco"]) * int(item["qtd"])
            total_pedido += subtotal
            c1, c2, c3 = st.columns([3, 2, 1], vertical_alignment="center")
            with c1:
                st.write(f"**{item['nome']}** · {item['tamanho']}")
            with c2:
                st.write(f"{item['qtd']} × R$ {item['preco']:.2f} = **R$ {subtotal:.2f}**")
            with c3:
                if st.button("Remover", key=f"del_cart_{idx}"):
                    st.session_state.carrinho.pop(idx)
                    st.rerun()
        st.markdown(f"### Total dos produtos: R$ {total_pedido:.2f}")
        st.markdown("### 🚚 Como você quer receber?")
        entrega = st.radio("Entrega", ["Retirar em mãos", "Receber por envio"], horizontal=True, key="entrega")
        taxa_envio = 0.0
        if entrega == "Receber por envio":
            st.caption("O frete será combinado com a loja antes do pagamento.")
            endereco = st.text_input("Cidade/CEP para combinar o envio")
        else:
            endereco = ""
            st.caption("A loja combinará com você o local e horário de retirada.")
        nome_cliente = st.text_input("Seu nome", key="checkout_nome")
        email_cliente = st.text_input("E-mail (necessário para checkout online)", key="checkout_email")
        st.markdown("### 💳 Forma de pagamento")
        forma_pagamento = st.radio("Pagamento", ["Pix", "Cartão (crédito/débito)"], horizontal=True, key="forma_pagamento")
        st.caption("Pagamento online seguro via Mercado Pago. O checkout só fica ativo após configurar o token da loja nos Secrets do Streamlit.")
        if st.button("🔒 Ir para pagamento seguro", use_container_width=True):
            token = st.secrets.get("MERCADO_PAGO_ACCESS_TOKEN", "")
            if not token:
                st.error("Checkout ainda não configurado. O administrador precisa adicionar MERCADO_PAGO_ACCESS_TOKEN em Settings → Secrets no Streamlit.")
            elif not nome_cliente.strip() or not email_cliente.strip() or ("@" not in email_cliente):
                st.error("Informe seu nome e um e-mail válido.")
            else:
                items = [{"title": item["nome"] + " (" + item["tamanho"] + ")", "quantity": int(item["qtd"]),
                          "unit_price": float(item["preco"]), "currency_id": "BRL"}
                         for item in st.session_state.carrinho]
                payload = {
                    "items": items,
                    "payer": {"name": nome_cliente.strip(), "email": email_cliente.strip()},
                    "statement_descriptor": "ISA HAMA BEADS",
                    "external_reference": "isa-hama-beads",
                    "metadata": {"entrega": entrega, "endereco_ou_cep": endereco, "forma_preferida": forma_pagamento},
                    "back_urls": {"success": "https://share.streamlit.io/", "failure": "https://share.streamlit.io/", "pending": "https://share.streamlit.io/"},
                    "auto_return": "approved"
                }
                try:
                    resp = requests.post("https://api.mercadopago.com/checkout/preferences",
                        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
                        json=payload, timeout=20)
                    if resp.ok:
                        checkout_url = resp.json().get("init_point")
                        if checkout_url:
                            st.success("Pedido preparado. Clique para concluir o pagamento no Mercado Pago.")
                            st.link_button("Pagar com segurança no Mercado Pago", checkout_url, use_container_width=True)
                        else:
                            st.error("O Mercado Pago não retornou o link de pagamento.")
                    else:
                        st.error(f"Falha ao criar checkout (HTTP {resp.status_code}). Confira o token e as configurações da conta Mercado Pago.")
                except requests.RequestException:
                    st.error("Não foi possível conectar ao Mercado Pago agora.")
        msg = "Olá! Quero combinar meu pedido da Isa Hama Beads:\n"
        for item in st.session_state.carrinho:
            msg += f"- {item['qtd']}x {item['nome']} ({item['tamanho']}) — R$ {item['preco']*item['qtd']:.2f}\n"
        msg += f"Total dos produtos: R$ {total_pedido:.2f}\nEntrega: {entrega}\n"
        if endereco:
            msg += f"Cidade/CEP: {endereco}\n"
        st.link_button("💬 Combinar pedido pelo WhatsApp", f"https://wa.me/{PHONE_WA}?text={urllib.parse.quote(msg)}", use_container_width=True)

st.markdown("---")
st.markdown("## 🎨 Catálogo de chaveiros")
f1, f2 = st.columns([2, 1])
with f1:
    busca = st.text_input("🔎 Buscar chaveiro", placeholder="Digite o nome do modelo")
with f2:
    filtro = st.selectbox("Categoria", ["Todas"] + sorted(set(p.get("categoria", "Chaveiros") for p in produtos)))
filtrados = [p for p in produtos if busca.lower() in p.get("nome", "").lower()]
if filtro != "Todas":
    filtrados = [p for p in filtrados if p.get("categoria", "Chaveiros") == filtro]
disponiveis = [p for p in filtrados if int(p.get("estoque", 0)) > 0]
if not filtrados:
    st.info("Nenhum chaveiro encontrado com esses filtros.")
else:
    cols = st.columns(3)
    for index, prod in enumerate(filtrados):
        with cols[index % 3]:
            st.markdown("<div class='product-card'>", unsafe_allow_html=True)
            if not mostrar_imagem(prod.get("imagem", "")):
                st.markdown("<div style='background:linear-gradient(135deg,#fff0f8,#f3eaff);border-radius:16px;padding:35px;text-align:center;font-size:3rem'>🧸🌸</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='pill'>{escape(str(prod.get('categoria','Chaveiros')))}</div><h3 style='margin:.7rem 0 .2rem'>{escape(str(prod['nome']))}</h3><div class='small-muted'>Tamanho: {escape(str(prod.get('tamanho','')))}</div><div class='price'>R$ {float(prod.get('preco',0)):.2f}</div>", unsafe_allow_html=True)
            if int(prod.get("estoque", 0)) > 0:
                if st.button("＋ Adicionar à sacolinha", key=f"add_{prod['id']}", use_container_width=True):
                    found = False
                    for item in st.session_state.carrinho:
                        if item["id"] == prod["id"]:
                            item["qtd"] += 1
                            found = True
                            break
                    if not found:
                        st.session_state.carrinho.append({"id": prod["id"], "nome": prod["nome"], "preco": float(prod["preco"]), "tamanho": prod.get("tamanho",""), "qtd": 1})
                    st.toast("Adicionado à sacolinha!")
                    st.rerun()
            else:
                st.button("Esgotado", key=f"out_{prod['id']}", disabled=True, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")
st.markdown("<div style='text-align:center;padding:14px;color:#806c89'><b>Isa Hama Beads</b><br>Feito à mão, peça por peça 🌸<br><small>Pedidos e informações pelo WhatsApp</small></div>", unsafe_allow_html=True)

# Admin
with st.expander("🔐 Acesso administrativo"):
    admin_password = st.secrets.get("ADMIN_PASSWORD", "")
    if not admin_password:
        st.warning("Configure ADMIN_PASSWORD em Settings → Secrets no Streamlit. Não deixe a senha no código porque o repositório é público.")
    senha = st.text_input("Senha do administrador", type="password")
    if admin_password and senha == admin_password:
        st.success("Painel administrativo liberado.")
        st.markdown("### Cadastrar chaveiro")
        with st.form("novo_prod_adm", clear_on_submit=True):
            nome = st.text_input("Nome do chaveiro")
            categoria = st.text_input("Categoria", value="Personagens")
            preco = st.number_input("Preço (R$)", min_value=0.0, value=8.0, step=1.0)
            tamanho = st.text_input("Tamanho", value="5 cm")
            estoque = st.number_input("Estoque", min_value=0, value=5, step=1)
            imagem_upload = st.file_uploader("Imagem do chaveiro", type=["png", "jpg", "jpeg"], key="imagem_novo_prod")
            salvar = st.form_submit_button("Cadastrar produto", use_container_width=True)
        if salvar:
            if not nome.strip():
                st.error("Informe o nome do produto.")
            else:
                novo_id = max([int(p.get("id",0)) for p in produtos], default=0) + 1
                produtos.append({"id": novo_id, "nome": nome.strip(), "categoria": categoria.strip() or "Chaveiros",
                                 "preco": float(preco), "tamanho": tamanho.strip(), "estoque": int(estoque),
                                 "imagem": imagem_data_url(imagem_upload)})
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
