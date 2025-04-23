import streamlit as st
from db_config import get_connection, criar_tabela
from storage_config import upload_imagem_stream

st.set_page_config(page_title="Cadastro de Produtos", layout="centered")
st.title("📦 Cadastro de Produtos")

criar_tabela()

# Formulário
with st.form("form_produto"):
    nome = st.text_input("Nome do produto")
    descricao = st.text_area("Descrição")
    preco = st.number_input("Preço", min_value=0.0, step=0.01, format="%.2f")
    imagem = st.file_uploader("Upload da imagem", type=["jpg", "jpeg", "png"])

    submitted = st.form_submit_button("Cadastrar")

    if submitted:
        if not (nome and descricao and preco and imagem):
            st.error("Preencha todos os campos e envie uma imagem.")
        else:
            url_imagem = upload_imagem_stream(imagem, imagem.name)

            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Produtos (nome, descricao, preco, url_imagem)
                VALUES (?, ?, ?, ?)
            """, (nome, descricao, preco, url_imagem))
            conn.commit()
            conn.close()

            st.success("✅ Produto cadastrado com sucesso!")

# Listagem
st.subheader("📋 Produtos cadastrados")
conn = get_connection()
cursor = conn.cursor()
cursor.execute("SELECT nome, descricao, preco, url_imagem FROM Produtos")
produtos = cursor.fetchall()
conn.close()

for produto in produtos:
    st.markdown(f"### {produto.nome} - R${produto.preco:.2f}")
    st.image(produto.url_imagem, width=200)
    st.markdown(produto.descricao)
    st.markdown("---")
