import streamlit as st
import google.generativeai as genai
from supabase import create_client
from datetime import datetime, date
import os

# =============================
# CONFIG
# =============================

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
GEMINI_KEY = st.secrets["GEMINI_API_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
genai.configure(api_key=GEMINI_KEY)

st.set_page_config(page_title="TechFox AI", page_icon="🦊", layout="wide")

# =============================
# FUNÇÕES
# =============================

def get_model():
    return genai.GenerativeModel("gemini-1.5-flash")

def criar_profile(user_id, email):
    supabase.table("profiles").insert({
        "id": user_id,
        "nome_loja": "Minha Assistência",
        "whatsapp": "",
        "plano": "free"
    }).execute()

def pegar_profile(user_id):
    res = supabase.table("profiles").select("*").eq("id", user_id).execute()
    return res.data[0] if res.data else None

def contar_uso_hoje(user_id, tabela):
    hoje = date.today().isoformat()
    res = supabase.table(tabela)\
        .select("*")\
        .eq("user_id", user_id)\
        .gte("created_at", hoje)\
        .execute()
    return len(res.data)

# =============================
# LOGIN
# =============================

if "user" not in st.session_state:
    st.session_state.user = None

if st.session_state.user is None:

    st.title("🦊 TechFox AI")

    tab1, tab2 = st.tabs(["Login", "Registrar"])

    with tab1:
        email = st.text_input("Email")
        senha = st.text_input("Senha", type="password")
        if st.button("Entrar"):
            try:
                user = supabase.auth.sign_in_with_password({
                    "email": email,
                    "password": senha
                })
                st.session_state.user = user
                st.rerun()
            except:
                st.error("Erro no login")

    with tab2:
        email = st.text_input("Novo Email")
        senha = st.text_input("Nova Senha", type="password")
        if st.button("Criar Conta"):
            try:
                user = supabase.auth.sign_up({
                    "email": email,
                    "password": senha
                })
                criar_profile(user.user.id, email)
                st.success("Conta criada!")
            except:
                st.error("Erro ao registrar")

# =============================
# PAINEL
# =============================

else:

    user_id = st.session_state.user.user.id
    profile = pegar_profile(user_id)

    with st.sidebar:
        st.subheader("⚙️ Perfil")

        nome_loja = st.text_input("Nome da Loja", profile["nome_loja"])
        whatsapp = st.text_input("WhatsApp", profile["whatsapp"])

        if st.button("Salvar Perfil"):
            supabase.table("profiles").update({
                "nome_loja": nome_loja,
                "whatsapp": whatsapp
            }).eq("id", user_id).execute()
            st.success("Atualizado")

        st.divider()
        st.write("Plano:", profile["plano"].upper())

        menu = st.radio("Ferramentas", [
            "Post Instagram",
            "Orçamento WhatsApp",
            "Ordem de Serviço"
        ])

        if st.button("Sair"):
            st.session_state.user = None
            st.rerun()

    model = get_model()

    # =============================
    # POST
    # =============================
    if menu == "Post Instagram":

        st.title("📱 Gerador de Post")

        aparelho = st.text_input("Aparelho")
        servico = st.text_input("Serviço")
        tempo = st.text_input("Tempo de Reparo")
        garantia = st.text_input("Garantia")

        if st.button("Gerar Post"):

            if profile["plano"] == "free" and contar_uso_hoje(user_id, "posts") >= 5:
                st.warning("Limite diário atingido. Faça upgrade para Pro.")
            else:

                prompt = f"""
                Crie um post profissional para Instagram da loja {nome_loja}.
                Reparo: {servico}
                Aparelho: {aparelho}
                Tempo: {tempo}
                Garantia: {garantia}
                Use emojis e hashtags.
                """

                res = model.generate_content(prompt)

                st.text_area("Resultado", res.text, height=300)

                supabase.table("posts").insert({
                    "user_id": user_id,
                    "aparelho": aparelho,
                    "servico": servico,
                    "conteudo": res.text
                }).execute()

    # =============================
    # ORÇAMENTO
    # =============================
    elif menu == "Orçamento WhatsApp":

        st.title("💬 Gerador de Orçamento")

        cliente = st.text_input("Cliente")
        modelo = st.text_input("Modelo")
        problema = st.text_area("Problema")
        valor = st.text_input("Valor")
        prazo = st.text_input("Prazo")

        if st.button("Gerar Orçamento"):

            if profile["plano"] == "free" and contar_uso_hoje(user_id, "orcamentos") >= 5:
                st.warning("Limite diário atingido.")
            else:

                prompt = f"""
                Crie mensagem profissional para WhatsApp.
                Loja: {nome_loja}
                Cliente: {cliente}
                Modelo: {modelo}
                Problema: {problema}
                Valor: R$ {valor}
                Prazo: {prazo}
                """

                res = model.generate_content(prompt)

                st.text_area("Mensagem", res.text, height=300)

                supabase.table("orcamentos").insert({
                    "user_id": user_id,
                    "cliente": cliente,
                    "modelo": modelo,
                    "valor": valor,
                    "mensagem": res.text
                }).execute()

    # =============================
    # ORDEM DE SERVIÇO
    # =============================
    elif menu == "Ordem de Serviço":

        st.title("📄 Ordem de Serviço")

        modelo = st.text_input("Modelo")
        imei = st.text_input("IMEI")
        estado = st.text_area("Estado do Aparelho")

        if st.button("Gerar O.S."):

            if profile["plano"] == "free" and contar_uso_hoje(user_id, "ordens_servico") >= 3:
                st.warning("Limite diário atingido.")
            else:

                prompt = f"""
                Gere uma ordem de serviço profissional.
                Loja: {nome_loja}
                Modelo: {modelo}
                IMEI: {imei}
                Estado: {estado}
                Inclua termo de responsabilidade.
                """

                res = model.generate_content(prompt)

                st.text_area("Ordem Gerada", res.text, height=300)

                supabase.table("ordens_servico").insert({
                    "user_id": user_id,
                    "modelo": modelo,
                    "imei": imei,
                    "estado": estado,
                    "resumo": res.text
                }).execute()
