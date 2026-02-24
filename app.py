import streamlit as st
import google.generativeai as genai
from supabase import create_client, Client
import streamlit.components.v1 as components

# --- 1. CONFIGURAÇÃO SUPABASE ---
SUPABASE_URL = "https://msitsrebkgekgqbuclqp.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1zaXRzcmVia2dla2dxYnVjbHFwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzA3NDE3MzgsImV4cCI6MjA4NjMxNzczOH0.AXZbP1hoCMCIwfHBH6iX98jy4XB2FoJp7P6i73ssq2k"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- 2. CONFIGURAÇÃO GEMINI (LÓGICA DE AUTO-DETECÇÃO) ---
API_KEY = "AIzaSyBFg4D-C9kYpZVF8TYLDZFMwF_GnBc6y5k"
genai.configure(api_key=API_KEY)

def get_model():
    """Busca automaticamente o melhor modelo disponível na sua conta"""
    try:
        # Lista todos os modelos que suportam geração de conteúdo
        modelos_disponiveis = [
            m.name for m in genai.list_models() 
            if 'generateContent' in m.supported_generation_methods
        ]
        
        # Prioridade: 1. Flash (mais rápido), 2. Pro (mais inteligente), 3. Qualquer um que sobrar
        for m in modelos_disponiveis:
            if "flash" in m: return genai.GenerativeModel(m)
        for m in modelos_disponiveis:
            if "pro" in m: return genai.GenerativeModel(m)
            
        return genai.GenerativeModel(modelos_disponiveis[0])
    except Exception as e:
        # Fallback de segurança caso a listagem falhe
        return genai.GenerativeModel('gemini-1.5-flash')

# --- 3. UI/UX TECHFOX PREMIUM ---
st.set_page_config(page_title="TechFox AI | Assistente Técnico", page_icon="🦊", layout="wide")

st.markdown("""
    <style>
    .stApp { background: #0f172a; color: #f1f5f9; }
    .tech-card {
        background: #1e293b;
        border: 1px solid #38bdf8;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(56, 189, 248, 0.1);
        margin-bottom: 20px;
    }
    .stButton>button {
        background: linear-gradient(90deg, #38bdf8 0%, #2563eb 100%) !important;
        color: white !important;
        font-weight: bold;
        border-radius: 8px;
        width: 100%;
        border: none;
        padding: 12px;
    }
    .output-box {
        background: #020617;
        color: #38bdf8;
        padding: 20px;
        border-radius: 8px;
        border-left: 5px solid #38bdf8;
        font-family: 'Inter', sans-serif;
    }
    h1, h2 { background: linear-gradient(to right, #38bdf8, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. FUNÇÃO COPIAR ---
def copy_button(text, key):
    safe_text = text.replace("`", "'").replace("\n", "\\n").replace('"', '\\"')
    html_code = f"""
    <button id="btn-{key}" onclick="copyToClipboard('{key}')" style="width: 100%; background: #020617; color: #38bdf8; border: 1px solid #38bdf8; padding: 10px; border-radius: 8px; font-weight: bold; cursor: pointer;"> 📋 COPIAR TEXTO </button>
    <script>
    function copyToClipboard(key) {{
        const text = "{safe_text}";
        navigator.clipboard.writeText(text).then(() => {{
            const btn = document.getElementById('btn-' + key);
            btn.innerHTML = '✅ COPIADO';
            setTimeout(() => {{ btn.innerHTML = '📋 COPIAR TEXTO'; }}, 2000);
        }});
    }}
    </script> """
    components.html(html_code, height=55)

# --- 5. LÓGICA DE LOGIN ---
if 'user' not in st.session_state: st.session_state.user = None

if st.session_state.user is None:
    c1, c2, c3 = st.columns([1, 1.2, 1])
    with c2:
        st.markdown("<h1 style='text-align: center;'>🦊 TechFox AI</h1>", unsafe_allow_html=True)
        aba_log, aba_cad = st.tabs(["🔒 Acesso", "✨ Criar Conta"])
        with aba_log:
            e = st.text_input("E-mail")
            s = st.text_input("Senha", type="password")
            if st.button("ACESSAR SISTEMA"):
                try:
                    res = supabase.auth.sign_in_with_password({"email": e, "password": s})
                    st.session_state.user = res
                    st.rerun()
                except: st.error("Dados incorretos.")
        with aba_cad:
            e_c = st.text_input("E-mail de Cadastro")
            s_c = st.text_input("Senha de Cadastro", type="password")
            if st.button("REGISTRAR AGORA"):
                try:
                    supabase.auth.sign_up({"email": e_c, "password": s_c})
                    st.success("Conta criada! Pode logar.")
                except Exception as ex: st.error(f"Erro: {ex}")
else:
    # --- 6. PAINEL DO TÉCNICO ---
    with st.sidebar:
        st.markdown("### ⚙️ Painel Fox")
        loja = st.text_input("Nome da Assistência", "Minha Assistência")
        contato = st.text_input("WhatsApp", placeholder="Ex: (11) 99999-9999")
        menu = st.radio("Selecione:", ["📱 Instagram", "💬 WhatsApp", "📄 O.S."])
        if st.button("🚪 Sair"):
            st.session_state.user = None
            st.rerun()

    if menu == "📱 Instagram":
        st.title("🚀 Post p/ Instagram")
        st.markdown('<div class="tech-card">', unsafe_allow_html=True)
        aparelho = st.text_input("Aparelho")
        servico = st.text_input("Serviço")
        st.markdown('</div>', unsafe_allow_html=True)

        if st.button("✨ GERAR POST"):
            with st.spinner("Gerando..."):
                try:
                    model = get_model()
                    res = model.generate_content(f"Crie um post de Instagram para {loja} sobre {servico} no {aparelho}.")
                    st.markdown(f'<div class="output-box">{res.text}</div>', unsafe_allow_html=True)
                    copy_button(res.text, "inst")
                except Exception as e: st.error(f"Erro: {e}")

    elif menu == "💬 WhatsApp":
        st.title("💰 Orçamento WhatsApp")
        st.markdown('<div class="tech-card">', unsafe_allow_html=True)
        cliente = st.text_input("Nome do Cliente")
        valor = st.text_input("Valor (R$)")
        st.markdown('</div>', unsafe_allow_html=True)

        if st.button("📤 GERAR ORÇAMENTO"):
            with st.spinner("Gerando..."):
                try:
                    model = get_model()
                    res = model.generate_content(f"Crie um orçamento para {cliente} na loja {loja} valor R$ {valor}.")
                    st.markdown(f'<div class="output-box">{res.text}</div>', unsafe_allow_html=True)
                    copy_button(res.text, "wpp")
                except Exception as e: st.error(f"Erro: {e}")
