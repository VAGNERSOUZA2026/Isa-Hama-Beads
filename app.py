import streamlit as st
import pandas as pd
import os
import json
import urllib.parse
from PIL import Image

# Configuração da página
st.set_page_config(
    page_title="Isa Hama Beads",
    page_icon="🎨",
    layout="centered"
)

# Estilização visual inspirada no design enviado (tons de rosa, roxo, cartões com bordas suaves)
st.markdown("""
    <style>
    .main {
        background-color: #FFF9FC;
    }
    .stButton>button {
        background: linear-gradient(135deg, #d946ef 0%, #a855f7 100%);
        color: white;
        border: none;
        border-radius: 12px;
        font-weight: bold;
        padding: 0.6rem 1rem;
        width: 100%;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #c026d3 0%, #9333ea 100%);
        color: white;
    }
    .card {
        background-color: white;
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 4px 12px rgba(217, 70, 239, 0.1);
        margin-bottom: 20px;
        border: 1px solid #fae8ff;
    }
    h1, h2, h3 {
        color: #701a75;
    }
    </style>
""", unsafe_allow_html=True)

# Arquivos de dados locais
DATA_FILE = "produtos.json"
IMG_DIR = "imagens_produtos"

if not os.path.exists(IMG_DIR):
    os.makedirs(IMG_DIR)

def carregar_produtos():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        dados_iniciais = [
            {"id": 1, "nome": "Homem Aranha", "categoria": "Personagens", "preco": 8.0, "tamanho": "5cm", "estoque": 10, "imagem": ""},
            {"id": 2, "nome": "Simon sprunki", "categoria": "Personagens", "preco": 8.0, "tamanho": "5cm", "estoque": 5, "imagem": ""}
        ]
        salvar_produtos(dados_iniciais)
        return dados_iniciais

def salvar_produtos(produtos):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(produtos, f, ensure_ascii=False, indent=4)

produtos = carregar_produtos()

# Inicializar carrinho na sessão se não existir
if 'carrinho' not in st.session_state:
    st.session_state.carrinho = []

# Cabeçalho com Logo e Carrinho Flutuante
col_logo, col_vazio, col_cart = st.columns([1, 2, 1])
with col_logo:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=80)
    else:
        st.markdown("🎨 **Isa Hama Beads**")

with col_cart:
    total_itens = sum(item['qtd'] for item in st.session_state.carrinho)
    if st.button(f"🛒 Bolsa ({total_itens})"):
        st.session_state.ver_carrinho = not st.session_state.get('ver_carrinho', False)

st.markdown("---")

# SEÇÃO: Criar seu chaveiro personalizado
st.markdown("""
<div class="card">
    <span style="background-color: #fae8ff; color: #a21caf; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: bold;">Feito especialmente para você</span>
    <h2 style="margin-top: 10px;">Crie seu chaveiro personalizado</h2>
    <p style="color: #6b7280; font-size: 14px;">Conte sua ideia e envie a referência na conversa do WhatsApp. O valor será combinado depois da análise do modelo.</p>
</div>
""", unsafe_allow_html=True)

with st.form("form_personalizado"):
    st.markdown("##### Foto de referência")
    foto_ref = st.file_uploader("Escolher arquivo", type=["png", "jpg", "jpeg"], label_visibility="collapsed")
    st.caption("A imagem será apenas pré-visualizada aqui. Você deverá enviá-la novamente na conversa do WhatsApp.")
    
    nome_personagem = st.text_input("Nome ou personagem desejado", placeholder="Ex.: Meu gato, Hello Kitty, logo da empresa...")
    
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        tamanho_opc = st.selectbox("Tamanho", ["5 cm", "7 cm", "10 cm", "Personalizado"])
    with col_t2:
        qtd_pers = st.number_input("Quantidade", min_value=1, value=1)
        
    cores_desejadas = st.text_input("Cores desejadas", placeholder="Ex.: rosa, branco e dourado")
    obs_modelo = st.text_area("Observações do modelo", placeholder="Conte detalhes, cores específicas, texto ou acabamento desejado...")
    
    enviar_orcamento = st.form_submit_button("Solicitar orçamento pelo WhatsApp")
    
    if enviar_orcamento:
        numero_whatsapp = "5531999999999" # Altere para o seu número com DDI e DDD
        
        mensagem = f"Olá! Gostaria de um orçamento para um *Chaveiro Personalizado*:\n\n"
        if nome_personagem:
            mensagem += f"- *Nome/Personagem:* {nome_personagem}\n"
        mensagem += f"- *Tamanho:* {tamanho_opc}\n- *Quantidade:* {qtd_pers}\n- *Cores:* {cores_desejadas}\n- *Observações:* {obs_modelo}\n\n*(Vou enviar a foto de referência aqui na conversa!)*"
        
        msg_codificada = urllib.parse.quote(mensagem)
        link_wa = f"https://wa.me/{numero_whatsapp}?text={msg_codificada}"
        
        st.success("Tudo pronto! Clique abaixo para abrir o WhatsApp e enviar os detalhes com a foto:")
        st.markdown(f'<a href="{link_wa}" target="_blank"><button style="background: linear-gradient(135deg, #25D366 0%, #128C7E 100%); color:white; padding:12px 20px; border:none; border-radius:12px; font-weight:bold; width:100%; text-align:center; text-decoration:none; display:block; margin-top:10px;">📲 Enviar Pedido no WhatsApp</button></a>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# SEÇÃO: Carrinho flutuante (se aberto)
if st.session_state.get('ver_carrinho', False):
    st.markdown("### 🛍️ Seu Carrinho de Compras")
    if not st.session_state.carrinho:
        st.info("Sua bolsa está vazia.")
    else:
        total_pedido = 0
        for idx, item in enumerate(st.session_state.carrinho):
            subtotal = item['preco'] * item['qtd']
            total_pedido += subtotal
            col_ci1, col_ci2, col_ci3 = st.columns([3, 2, 1])
            with col_ci1:
                st.write(f"**{item['nome']}** ({item['tamanho']})")
            with col_ci2:
                st.write(f"{item['qtd']}x R$ {item['preco']:.2f} = R$ {subtotal:.2f}")
            with col_ci3:
                if st.button("❌", key=f"del_cart_{idx}"):
                    st.session_state.carrinho.pop(idx)
                    st.rerun()
        
        st.markdown(f"**Total Geral:** R$ {total_pedido:.2f}")
        telefone_zap = "5531999999999" # Altere para o seu WhatsApp
        
        msg_carrinho = "Olá! Gostaria de fechar o seguinte pedido:\n\n"
        for item in st.session_state.carrinho:
            msg_carrinho += f"- {item['qtd']}x {item['nome']} ({item['tamanho']}) - R$ {item['preco']*item['qtd']:.2f}\n"
        msg_carrinho += f"\n*Total:* R$ {total_pedido:.2f}"
        
        link_carrinho = f"https://wa.me/{telefone_zap}?text={urllib.parse.quote(msg_carrinho)}"
        st.markdown(f'<a href="{link_carrinho}" target="_blank"><button style="background: linear-gradient(135deg, #25D366 0%, #128C7E 100%); color:white; padding:12px 20px; border:none; border-radius:12px; font-weight:bold; width:100%; text-align:center; text-decoration:none; display:block;">📲 Finalizar Pedido no WhatsApp</button></a>', unsafe_allow_html=True)
    st.markdown("---")

# SEÇÃO: Catálogo de Produtos
st.markdown("## Catálogo")

# Filtros e Barra de Pesquisa
busca = st.text_input("🔍 Buscar chaveiro...", placeholder="Ex.: Homem Aranha, Simon...")
filtro_aba = st.radio("Filtros", ["Todos", "Disponíveis", "Esgotados", "Personagens"], horizontal=True, label_visibility="collapsed")

# Filtragem de produtos
produtos_filtrados = produtos
if busca:
    produtos_filtrados = [p for p in produtos_filtrados if busca.lower() in p['nome'].lower()]

if filtro_aba == "Disponíveis":
    produtos_filtrados = [p for p in produtos_filtrados if p['estoque'] > 0]
elif filtro_aba == "Esgotados":
    produtos_filtrados = [p for p in produtos_filtrados if p['estoque'] == 0]
elif filtro_aba == "Personagens":
    produtos_filtrados = [p for p in produtos_filtrados if p.get('categoria') == "Personagens"]

# Exibição dos produtos em grade de colunas
cols = st.columns(2)
for index, prod in enumerate(produtos_filtrados):
    with cols[index % 2]:
        st.markdown(f"""
        <div style="background: white; padding: 15px; border-radius: 16px; border: 1px solid #fae8ff; box-shadow: 0 2px 8px rgba(0,0,0,0.05); margin-bottom: 15px;">
            <span style="background: #f3e8ff; color: #6b21a8; padding: 2px 8px; border-radius: 10px; font-size: 10px; font-weight: bold;">{prod.get('categoria', 'Chaveiro')}</span>
            <h4 style="margin: 8px 0 4px 0; color: #4a044e;">{prod['nome']}</h4>
            <p style="color: #6b7280; font-size: 12px; margin-bottom: 8px;">Tamanho {prod['tamanho']}</p>
            <p style="color: #701a75; font-weight: bold; font-size: 16px; margin-bottom: 10px;">R$ {prod['preco']:.2f}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Botão de adicionar ao carrinho
        if st.button("➕ Adicionar", key=f"add_{prod['id']}"):
            encontrado = False
            for item in st.session_state.carrinho:
                if item['id'] == prod['id']:
                    item['qtd'] += 1
                    encontrado = True
                    break
            if not encontrado:
                st.session_state.carrinho.append({
                    "id": prod['id'],
                    "nome": prod['nome'],
                    "preco": prod['preco'],
                    "tamanho": prod['tamanho'],
                    "qtd": 1
                })
            st.success(f"Adicionado!")
            st.rerun()

st.markdown("---")

# Rodapé e Acesso Administrativo
st.markdown("""
<div style="text-align: center; color: #701a75; font-size: 14px;">
    <b>Isa Hama Beads</b><br>
    Chaveiros artesanais em Hama Beads 🌸
</div>
""", unsafe_allow_html=True)

with st.expander("Acesso administrativo"):
    senha_adm = st.text_input("Senha do Administrador", type="password")
    if senha_adm == "isa123":
        st.success("Painel Liberado!")
        
        st.subheader("Gerenciar / Cadastrar Produtos")
        with st.form("novo_prod_adm"):
            novo_nome = st.text_input("Nome do Chaveiro")
            novo_cat = st.text_input("Categoria", value="Personagens")
            novo_preco = st.number_input("Preço (R$)", value=8.0)
            novo_tam = st.text_input("Tamanho", value="5cm")
            novo_est = st.number_input("Estoque", value=5, min_value=0)
            
            cadastrar_btn = st.form_submit_button("Cadastrar Chaveiro")
            if cadastrar_btn:
                novo_id = max([p['id'] for p in produtos]) + 1 if produtos else 1
                produtos.append({
                    "id": novo_id,
                    "nome": novo_nome,
                    "categoria": novo_cat,
                    "preco": novo_preco,
                    "tamanho": novo_tam,
                    "estoque": novo_est,
                    "imagem": ""
                })
                salvar_produtos(produtos)
                st.success("Produto cadastrado com sucesso!")
                st.rerun()
                
        st.subheader("Excluir / Editar Estoque")
        for p in produtos:
            col_ex1, col_ex2 = st.columns([3, 1])
            with col_ex1:
                st.write(f"**{p['nome']}** - Estoque: {p['estoque']}")
            with col_ex2:
                if st.button("Excluir", key=f"del_prod_{p['id']}"):
                    produtos = [x for x in produtos if x['id'] != p['id']]
                    salvar_produtos(produtos)
                    st.rerun()
    elif senha_adm:
        st.error("Senha incorreta.")
