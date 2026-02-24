import streamlit as st
import google.generativeai as genai
from supabase import create_client, Client
import streamlit.components.v1 as components

# --- 1. CONFIGURAÇÃO SUPABASE ---
# Mantendo suas credenciais para o sistema de login funcionar
SUPABASE_URL = "https://msitsrebkgekgqbuclqp.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1zaXRzcmVia2dla2dxYnVjbHFwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzA3NDE3MzgsImV4cCI6MjA4NjMxNzczOH0.AXZbP1hoCMCIwfHBH6iX98jy4XB2FoJp7P6i73ssq2k"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- 2. CONFIGURAÇÃO GEMINI (CORRIGIDA) ---
API_KEY = "AIzaSyBFg4D-C9kYpZVF8TYLDZFMwF_GnBc6y5k"
genai.configure(api_key=API_KEY)

def get_model():
    # Versão corrigida para evitar o erro de "NotFound"
    try:
        return genai.GenerativeModel('gemini-1.5-flash-latest')
    except:
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
        transition: 0.3s;
    }
    
    .output-box {
        background: #020617;
        color: #38bdf8;
        padding: 20px;
        border-radius: 8px;
        border-left: 5px solid #38bdf8;
        font-family: 'Inter', sans-serif;
        line-height: 1.6;
        margin-top: 15px;
    }
    
    /* Títulos em Degradê */
    h1, h2, h3 {
        background: linear-gradient(to right, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
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
            btn.innerHTML = '✅ COPIADO COM SUCESSO';
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
        st.markdown("<p style='text-align: center; color: #94a3b8;'>Inteligência Artificial para Técnicos de Celular</p>", unsafe_allow_html=True)
        
        tab_log, tab_cad = st.tabs(["🔒 Acesso", "✨ Criar Conta"])
        with tab_log:
            e = st.text_input("E-mail", key="l_e")
            s = st.text_input("Senha", type="password", key="l_s")
            if st.button("ACESSAR SISTEMA"):
                try:
                    res = supabase.auth.sign_in_with_password({"email": e, "password": s})
                    st.session_state.user = res
                    st.rerun()
                except: st.error("E-mail ou senha incorretos.")
        with tab_cad:
            e_c = st.text_input("Seu melhor E-mail", key="c_e")
            s_c = st.text_input("Crie uma Senha", type="password", key="c_s")
            if st.button("REGISTRAR AGORA"):
                try:
                    supabase.auth.sign_up({"email": e_c, "password": s_c})
                    st.success("Conta criada! Pode fazer login.")
                except Exception as ex: st.error(f"Erro: {ex}")
else:
    # --- 6. PAINEL DO TÉCNICO ---
    with st.sidebar:
        st.markdown("### ⚙️ Painel Fox")
        loja = st.text_input("Nome da Assistência", "Minha Assistência")
        contato = st.text_input("WhatsApp para Clientes", placeholder="Ex: (11) 99999-9999")
        st.divider()
        menu = st.radio("Selecione uma Função:", [
            "📱 Posts p/ Instagram", 
            "💬 Orçamento WhatsApp", 
            "📄 Ordem de Serviço"
        ])
        if st.button("🚪 Sair"):
            st.session_state.user = None
            st.rerun()

    # --- FERRAMENTA: INSTAGRAM ---
    if menu == "📱 Posts p/ Instagram":
        st.title("🚀 Gerador de Conteúdo")
        st.markdown("Crie posts persuasivos que mostram seu profissionalismo.")
        
        with st.container():
            st.markdown('<div class="tech-card">', unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                aparelho = st.text_input("Modelo do Aparelho", placeholder="Ex: iPhone 11")
                servico = st.selectbox("Serviço Realizado", ["Troca de Tela", "Troca de Bateria", "Reparo em Placa", "Banho Químico", "Conector de Carga"])
            with c2:
                tempo = st.text_input("Tempo de Reparo", "45 min")
                garantia = st.selectbox("Garantia", ["30 Dias", "90 Dias", "6 Meses"])
            st.markdown('</div>', unsafe_allow_html=True)

        if st.button("✨ GERAR POST PROFISSIONAL"):
            with st.spinner("TechFox está escrevendo..."):
                try:
                    model = get_model()
                    prompt = (f"Crie um post para Instagram de uma assistência técnica chamada {loja}. "
                              f"Fale sobre o conserto de {servico} no {aparelho}. "
                              f"Destaque o prazo de {tempo} e a garantia de {garantia}. "
                              f"Use emojis técnicos e CTAs para o WhatsApp {contato}.")
                    res = model.generate_content(prompt)
                    st.markdown(f'<div class="output-box">{res.text}</div>', unsafe_allow_html=True)
                    copy_button(res.text, "post_fox")
                except Exception as e: st.error(f"Erro na IA: {e}")

    # --- FERRAMENTA: WHATSAPP (A QUE DEU ERRO) ---
    elif menu == "💬 Orçamento WhatsApp":
        st.title("💰 Orçamento Profissional")
        st.markdown("Transforme orçamentos em vendas com textos estruturados.")
        
        with st.container():
            st.markdown('<div class="tech-card">', unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                cliente = st.text_input("Nome do Cliente")
                cel_modelo = st.text_input("Aparelho")
            with c2:
                valor_orc = st.text_input("Valor Total (R$)")
                prazo_orc = st.text_input("Prazo de Entrega")
            defeito = st.text_area("Diagnóstico Técnico (O que será feito?)")
            st.markdown('</div>', unsafe_allow_html=True)

        if st.button("📤 GERAR ORÇAMENTO PARA WHATSAPP"):
            with st.spinner("Calculando orçamento..."):
                try:
                    model = get_model()
                    prompt = (f"Crie uma mensagem profissional de orçamento para WhatsApp. "
                              f"Loja: {loja}. Cliente: {cliente}. Aparelho: {cel_modelo}. "
                              f"Serviço: {defeito}. Valor: R$ {valor_orc}. Prazo: {prazo_orc}. "
                              f"Seja educado e passe confiança técnica.")
                    res = model.generate_content(prompt)
                    st.markdown(f'<div class="output-box">{res.text}</div>', unsafe_allow_html=True)
                    copy_button(res.text, "zap_fox")
                except Exception as e: st.error(f"Erro na IA: {e}")

    # --- FERRAMENTA: O.S. ---
    elif menu == "📄 Ordem de Serviço":
        st.title("📄 Ordem de Serviço (Rascunho)")
        st.markdown("Registre a entrada de aparelhos com precisão.")
        
        with st.container():
            st.markdown('<div class="tech-card">', unsafe_allow_html=True)
            st.text_input("IMEI / Serial")
            st.multiselect("Checklist de Entrada", ["Liga", "Touch OK", "Câmeras OK", "Carregando", "Microfone OK"])
            st.text_area("Estado Físico (Riscos, amassados, etc)")
            st.button("SALVAR REGISTRO (EM BREVE PDF)")
            st.markdown('</div>', unsafe_allow_html=True)
