import streamlit as st
import json
import os
import base64
import urllib.parse
from html import escape

st.set_page_config(page_title="Isa Hama Beads | Chaveiros artesanais", page_icon="🌸", layout="wide")

DATA_FILE = "produtos.json"
PHONE_WA = "5531989684010"
LOGO_FILE = "logo.png"

# Paleta moderna inspirada em Hama Beads
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Playfair+Display:wght@600;700&display=swap');
:root { --pink:#f04b9b; --pink-dark:#c82e7d; --purple:#7545a8; --purple-dark:#4b285f; --ink:#30243a; --cream:#fff8fc; --line:#f3d6e8; }
.stApp { background: radial-gradient(ellipse at 8% 0%,#ffe5f3 0,transparent 34%), radial-gradient(ellipse at 100% 12%,#eee2ff 0,transparent 30%), linear-gradient(180deg,#fffafd 0%,#fff 55%,#fff8fc 100%); color:var(--ink); }
.block-container { max-width: 1220px; padding-top: 1.6rem; padding-bottom: 3rem; }
h1,h2,h3 { color:var(--purple-dark); font-family:'Playfair Display',serif; letter-spacing:-.02em; }
h2 { margin-top:1.4rem; }
p,div,label { font-family:'DM Sans',sans-serif; }
[data-testid="stHeader"] { background:rgba(255,250,253,.88); }
.stButton>button, .stFormSubmitButton>button, .stLinkButton> a {
  border:0; border-radius:14px; padding:.72rem 1rem; font-weight:800;
  color:white; background:linear-gradient(115deg,var(--pink),#a34ed0);
  box-shadow:0 8px 20px #d85b9b2b; transition:transform .18s, box-shadow .18s;
}
.stButton>button:hover,.stFormSubmitButton>button:hover,.stLinkButton> a:hover { color:white; transform:translateY(-2px); box-shadow:0 12px 26px #d85b9b42; }
.stTextInput input,.stTextArea textarea,.stNumberInput input,.stSelectbox div[data-baseweb="select"] { border-radius:12px; border-color:#e9c7df; }
div[data-testid="stMetric"], div[data-testid="stVerticalBlockBorderWrapper"] {
  border:1px solid var(--line); border-radius:20px; background:rgba(255,255,255,.92); padding:14px;
  box-shadow:0 8px 26px #4b285f08;
}
.hero {
  position:relative; overflow:hidden; border-radius:30px; padding:clamp(24px,4vw,40px);
  background:linear-gradient(130deg,#fff0f8 0%,#f0e5ff 55%,#fff5e8 100%);
  border:1px solid #f4d2e6; box-shadow:0 18px 50px #6d3a7c16; margin-bottom:22px;
}
.hero:after { content:""; position:absolute; width:250px;height:250px;border-radius:50%;
  right:-80px;top:-90px;background:radial-gradient(circle,#e84d9b30,transparent 68%); pointer-events:none; }
.hero-title { font-family:'Playfair Display',serif; color:var(--purple-dark); font-size:clamp(2rem,4vw,3.2rem); line-height:1.08; margin:.5rem 0; }
.hero-sub { color:#6d5b76; font-size:1.04rem; max-width:620px; line-height:1.7; }
.pill { display:inline-block; padding:7px 13px; border-radius:999px; background:#fff; color:var(--pink-dark); font-weight:800; font-size:.8rem; border:1px solid #f2cce1; }
.product-card { border:1px solid var(--line); border-radius:22px; background:white; padding:16px; box-shadow:0 10px 28px #4b285f0d; }
.price { color:var(--pink-dark); font-size:1.3rem; font-weight:800; }
.small-muted { color:#82738a; font-size:.9rem; }
div[data-testid="stImage"] img { border-radius:16px; }
div[data-testid="stExpander"] { border:1px solid var(--line); border-radius:18px; background:#fffafd; }
div[data-testid="stForm"] { border:1px solid #f1d8e8; border-radius:18px; padding:18px; background:#fff; }
@keyframes shimmer { 0%{background-position:0% 50%} 100%{background-position:200% 50%} }
.animated-strip { height:5px;border-radius:20px;background:linear-gradient(90deg,#e84d9b,#8e58bd,#f5b7d8,#e84d9b);background-size:200% 100%;animation:shimmer 5s linear infinite;margin:10px 0 22px; }
@media (max-width: 700px) { .block-container { padding-left:1rem; padding-right:1rem; } .hero { padding:22px; border-radius:22px; } }
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

# Cabeçalho único: uma só logo, inteira e sem duplicação
hero_left, hero_right = st.columns([1.5, 1], vertical_alignment="center")
with hero_left:
    st.markdown("""
    <section class="hero">
      <span class="pill">✦ FEITO À MÃO, COM CRIATIVIDADE</span>
      <div class="hero-title">Isa Hama Beads</div>
      <p class="hero-sub">Chaveiros artesanais coloridos, personalizados e cheios de personalidade.</p>
      <div style="height:1px;background:#f0cce2;margin:18px 0"></div>
      <span class="pill">🌈 Seu estilo em pequenas peças</span>
      <div style="font-family:'Playfair Display',serif;color:#4b285f;font-size:clamp(1.8rem,3vw,2.7rem);line-height:1.12;margin:.7rem 0">Pequenos detalhes.<br>Grandes ideias.</div>
      <p class="hero-sub">Escolha seu chaveiro favorito ou peça uma criação exclusiva feita com Hama Beads.</p>
      <p style="color:#7545a8;font-weight:700">💗 Presentes criativos • Personagens • Modelos personalizados</p>
    </section>
    """, unsafe_allow_html=True)
with hero_right:
    if os.path.exists(LOGO_FILE):
        st.image(LOGO_FILE, width=340)
    else:
        st.markdown("<div class='hero' style='text-align:center;font-size:5rem'>🧸🌸✨<p style='font-size:1rem'>Criatividade em cada miçanga</p></div>", unsafe_allow_html=True)

# Personalização fica recolhida até o cliente clicar
with st.expander("✨ Personalizar meu chaveiro", expanded=False):
    st.markdown("Conte sua ideia e envie a referência pelo WhatsApp. O valor será combinado após avaliar o modelo.")
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

# Sacolinha / pedido sem login, e-mail ou checkout Mercado Pago
st.markdown("## 🛍️ Sua sacolinha")
st.session_state.ver_carrinho = st.toggle("Mostrar carrinho", value=st.session_state.ver_carrinho)
if st.session_state.ver_carrinho:
    if not st.session_state.carrinho:
        st.info("Sua sacolinha está vazia. Adicione um chaveiro do catálogo.")
    else:
        total_pedido = sum(float(item["preco"]) * int(item["qtd"]) for item in st.session_state.carrinho)
        for idx, item in enumerate(st.session_state.carrinho):
            subtotal = float(item["preco"]) * int(item["qtd"])
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
        st.markdown("### 📦 Dados do pedido")
        with st.form("form_finalizar_pedido"):
            nome_cliente = st.text_input("Nome do cliente", placeholder="Seu nome")
            telefone_cliente = st.text_input("Telefone/WhatsApp", placeholder="DDD + número")
            entrega = st.radio("Como deseja receber?", ["Retirar em mãos", "Receber por envio"], horizontal=True)
            endereco = ""
            if entrega == "Receber por envio":
                endereco = st.text_input("CEP, cidade e endereço para combinar o envio")
            observacoes_pedido = st.text_area("Observações (opcional)", placeholder="Detalhes do pedido")
            enviar_pedido = st.form_submit_button("📲 Preparar pedido no WhatsApp", use_container_width=True)

        if enviar_pedido:
            if not nome_cliente.strip() or not telefone_cliente.strip():
                st.error("Preencha seu nome e telefone para preparar o pedido.")
            elif entrega == "Receber por envio" and not endereco.strip():
                st.error("Informe o CEP/cidade ou endereço para combinar o envio.")
            else:
                mensagem = "Olá! Quero fazer este pedido na Isa Hama Beads:\n"
                for item in st.session_state.carrinho:
                    mensagem += f"- {item['qtd']}x {item['nome']} ({item['tamanho']}) — R$ {float(item['preco'])*int(item['qtd']):.2f}\n"
                mensagem += f"Total dos produtos: R$ {total_pedido:.2f}\n"
                mensagem += f"Cliente: {nome_cliente.strip()}\nTelefone: {telefone_cliente.strip()}\nEntrega: {entrega}\n"
                if endereco:
                    mensagem += f"Endereço/CEP: {endereco.strip()}\n"
                if observacoes_pedido.strip():
                    mensagem += f"Observações: {observacoes_pedido.strip()}\n"
                st.session_state.mensagem_pedido_whatsapp = mensagem
                st.success("Pedido preenchido. Confira os dados e envie pelo WhatsApp.")
                st.link_button("Enviar pedido pelo WhatsApp", f"https://wa.me/{PHONE_WA}?text={urllib.parse.quote(mensagem)}", use_container_width=True)

        st.info("Após enviar o pedido pelo WhatsApp, a loja combinará a forma de pagamento diretamente com você.")

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
