import streamlit as st
import pandas as pd
import os
import json
import urllib.parse

# Configuração da página do aplicativo
st.set_page_config(
    page_title="Isa Hama Beads",
    page_icon="🎨",
    layout="wide"
)

# Arquivo JSON local para salvar os produtos e estoques
DATA_FILE = "produtos.json"

def carregar_produtos():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        # Produtos iniciais baseados nos modelos da logo (Stitch, Girassol, Hello Kitty, Pokébola, Panda)[cite: 1]
        dados_iniciais = [
            {"id": 1, "nome": "Chaveiro Stitch", "preco": 15.0, "estoque": 5},
            {"id": 2, "nome": "Chaveiro Girassol", "preco": 12.0, "estoque": 3},
            {"id": 3, "nome": "Chaveiro Hello Kitty", "preco": 15.0, "estoque": 4},
            {"id": 4, "nome": "Chaveiro Pokébola", "preco": 10.0, "estoque": 8},
            {"id": 5, "nome": "Chaveiro Panda", "preco": 15.0, "estoque": 2}
        ]
        salvar_produtos(dados_iniciais)
        return dados_iniciais

def salvar_produtos(produtos):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(produtos, f, ensure_ascii=False, indent=4)

produtos = carregar_produtos()

# Exibição da Logo e Cabeçalho
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True)
    else:
        st.title("💖 Isa Hama Beads 💖")
        st.markdown("<p style='text-align: center;'>Chaveiros artesanais feitos com muito carinho!</p>", unsafe_allow_html=True) #[cite: 1]

st.markdown("---")

# Menu de Navegação na Barra Lateral
menu = st.sidebar.selectbox("Menu Principal", ["Catálogo de Chaveiros", "Fazer Pedido / Orçamento", "Painel Administrativo"])

# 1. CATÁLOGO DE PRODUTOS
if menu == "Catálogo de Chaveiros":
    st.header("✨ Nossos Chaveiros Disponíveis")
    st.markdown("Confira os modelos prontos ou escolha sua inspiração para encomendar o seu!")
    
    cols = st.columns(3)
    for index, prod in enumerate(produtos):
        with cols[index % 3]:
            st.subheader(prod["nome"])
            st.write(f"**Preço:** R$ {prod['preco']:.2f}")
            st.write(f"**Estoque:** {prod['estoque']} unidades")
            if prod["estoque"] > 0:
                st.success("Disponível a pronta entrega!")
            else:
                st.warning("Sob encomenda")
            st.markdown("---")

# 2. FAZER PEDIDO / ORÇAMENTO
elif menu == "Fazer Pedido / Orçamento":
    st.header("🛍️ Monte seu Pedido ou Orçamento")
    st.markdown("Preencha os dados abaixo. O pedido será enviado diretamente para o nosso WhatsApp com resposta rápida! 🚀")

    with st.form("form_pedido"):
        nome_cliente = st.text_input("Seu Nome:")
        telefone_cliente = st.text_input("Seu WhatsApp (com DDD):")
        
        tipo_pedido = st.radio("Como deseja fazer seu pedido?", ["Escolher do Catálogo", "Enviar Modelo Personalizado (Foto própria)"])
        
        produto_escolhido = ""
        if tipo_pedido == "Escolher do Catálogo":
            nomes_prods = [p["nome"] for p in produtos]
            produto_escolhido = st.selectbox("Selecione o Chaveiro:", nomes_prods)
        else:
            st.info("💡 Dica: Descreva bem o modelo, tema ou envie os detalhes visuais no campo de observações abaixo.")
        
        tamanho = st.text_input("Tamanho aproximado (Ex: 5x5 cm):")
        cores = st.text_input("Cores principais desejadas:")
        quantidade = st.number_input("Quantidade:", min_value=1, value=1)
        observacoes = st.text_area("Observações ou detalhes do modelo:")
        
        enviar = st.form_submit_button("Gerar Mensagem para o WhatsApp")
        
        if enviar:
            if not nome_cliente or not telefone_cliente:
                st.warning("Por favor, preencha seu Nome e WhatsApp antes de continuar.")
            else:
                # Substitua abaixo pelo seu número de WhatsApp com DDI e DDD (Ex: 5531999999999)
                numero_whatsapp = "5531999999999" 
                
                if tipo_pedido == "Escolher do Catálogo":
                    mensagem = f"Olá! Meu nome é *{nome_cliente}*.\nGostaria de encomendar:\n- *Produto:* {produto_escolhido}\n- *Quantidade:* {quantidade}\n- *Tamanho:* {tamanho}\n- *Cores:* {cores}\n- *Obs:* {observacoes}"
                else:
                    mensagem = f"Olá! Meu nome é *{nome_cliente}*.\nGostaria de um orçamento para um *Modelo Personalizado*:\n- *Quantidade:* {quantidade}\n- *Tamanho:* {tamanho}\n- *Cores:* {cores}\n- *Obs:* {observacoes}"
                
                msg_codificada = urllib.parse.quote(mensagem)
                link_wa = f"https://wa.me/{numero_whatsapp}?text={msg_codificada}"
                
                st.success("Tudo pronto! Clique no botão abaixo para enviar seu pedido via WhatsApp:")
                st.markdown(f'<a href="{link_wa}" target="_blank"><button style="background-color:#25D366; color:white; padding:12px 20px; border:none; border-radius:8px; font-weight:bold; font-size:16px; cursor:pointer;">📲 Enviar Pedido no WhatsApp</button></a>', unsafe_allow_html=True)

# 3. PAINEL ADMINISTRATIVO
elif menu == "Painel Administrativo":
    st.header("⚙️ Painel Administrativo - Isa Hama Beads")
    st.markdown("Área restrita para atualizar estoques e gerenciar produtos.")
    
    senha = st.text_input("Digite a senha de acesso:", type="password")
    
    # Senha padrão de exemplo (você pode alterar para a que preferir)
    SENHA_MESTRE = "isa123"
    
    if senha == SENHA_MESTRE:
        st.success("Acesso autorizado com sucesso!")
        
        st.subheader("📦 Atualizar Produtos e Estoques Existentes")
        for i, p in enumerate(produtos):
            with st.expander(f"{p['nome']} (Estoque atual: {p['estoque']})"):
                novo_nome = st.text_input("Nome do Chaveiro", value=p["nome"], key=f"name_{i}")
                novo_preco = st.number_input("Preço (R$)", value=float(p["preco"]), key=f"price_{i}")
                novo_estoque = st.number_input("Estoque", value=int(p["estoque"]), key=f"stock_{i}")
                
                if st.button("Salvar Alterações", key=f"save_{i}"):
                    produtos[i]["nome"] = novo_nome
                    produtos[i]["preco"] = novo_preco
                    produtos[i]["estoque"] = novo_estoque
                    salvar_produtos(produtos)
                    st.success("Produto atualizado com sucesso!")
                    st.rerun()

        st.markdown("---")
        st.subheader("➕ Cadastrar Novo Chaveiro")
        with st.form("form_novo_produto"):
            nome_novo = st.text_input("Nome do Novo Chaveiro")
            preco_novo = st.number_input("Preço (R$)", min_value=0.0, value=15.0)
            estoque_novo = st.number_input("Quantidade inicial em Estoque", min_value=0, value=5)
            
            cadastrar = st.form_submit_button("Adicionar ao Catálogo")
            if cadastrar:
                novo_id = max([p["id"] for p in produtos]) + 1 if produtos else 1
                produtos.append({
                    "id": novo_id,
                    "nome": nome_novo,
                    "preco": preco_novo,
                    "estoque": estoque_novo
                })
                salvar_produtos(produtos)
                st.success("Novo chaveiro cadastrado com sucesso!")
                st.rerun()
                
    elif senha != "":
        st.error("Senha incorreta. Tente novamente.")
