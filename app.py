import streamlit as st
import google.generativeai as genai
from supabase import create_client, Client
import streamlit.components.v1 as components

# --- 1. CONFIGURAÇÃO SUPABASE ---
SUPABASE_URL = "https://msitsrebkgekgqbuclqp.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1zaXRzcmVia2dla2dxYnVjbHFwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzA3NDE3MzgsImV4cCI6MjA4NjMxNzczOH0.AXZbP1hoCMCIwfHBH6iX98jy4XB2FoJp7P6i73ssq2k"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- 2. CONFIGURAÇÃO GEMINI ---
API_KEY = "AIzaSyBFg4D-C9kYpZVF8TYLDZFMwF_GnBc6y5k"
genai.configure(api_key=API_KEY)

def get_model():
    try:
        modelos = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        for m in modelos:
            if "flash" in m: return genai.GenerativeModel(m)
        return genai.GenerativeModel(modelos[0])
    except: return genai.GenerativeModel('gemini-1.5-flash')

# --- 3. UI/UX TECHFOX PREMIUM (VISUAL DIFERENTE) ---
st.set_page_config(page_title="TechFox AI | Assistente Técnico", page_icon="🦊", layout="wide")

st.markdown("""
    <style>
    /* Estilo Dark Metal para Tecnologia */
    .stApp {
        background: #0f172a;
        color: #f1f5f9;
    }
    
    /* Cards com bordas em Neon Blue */
    .tech-card {
        background: #1e293b;
        border: 1px solid #38bdf8;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(56, 189, 248, 0.1);
        margin-bottom: 20px;
    }
    
    /* Botões estilo "High-Tech" */
    .stButton>button {
        background: #38bdf8 !important;
        color: #0f172a !important;
        font-weight: bold;
        border-radius: 8px;
        width: 100%;
        border: none;
        padding: 15px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background: #7dd3fc !important;
        box-shadow: 0 0 15px #38bdf8;
    }
    
    /* Estilo para as mensagens geradas */
    .output-box {
        background: #020617;
        color: #38bdf8;
        padding: 20px;
        border-radius: 8px;
        border-left: 5px solid #38bdf8;
        font-family: 'Courier New', monospace;
        margin-top: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. FUNÇÃO COPIAR ---
def copy_button(text, key):
    safe_text = text.replace("`", "'").replace("\n", "\\n").replace('"', '\\"')
    html_code = f"""
    <button id="btn-{key}" onclick="copyToClipboard('{key}')" style="width: 100%; background: #1e293b; color: #38bdf8; border: 1px solid #38bdf8; padding: 10px; border-radius: 8px; font-weight: bold; cursor: pointer;"> 📋 COPIAR </button>
    <script>
    function copyToClipboard(key) {{
        const text = "{safe_text}";
        navigator.clipboard.writeText(text).then(() => {{
            const btn = document.getElementById('btn-' + key);
            btn.innerHTML = '✅ COPIADO';
            setTimeout(() => {{ btn.innerHTML = '📋 COPIAR'; }}, 2000);
        }});
    }}
    </script> """
    components.html(html_code, height=55)

# --- 5. LOG LOGIN (DIFERENTE DO CHEF) ---
if 'user' not in st.session_state: st.session_state.user = None

if st.session_state.user is None:
    c1, c2, c3 = st.columns([1, 1.2, 1])
    with c2:
        st.markdown("<h1 style='text-align: center; color: #38bdf8;'>🦊 TechFox AI</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>Painel de Inteligência para Assistência Técnica</p>", unsafe_allow_html=True)
        
        tab_log, tab_cad = st.tabs(["Acesso Técnico", "Registrar Loja"])
        with tab_log:
            e = st.text_input("E-mail", key="l_e")
            s = st.text_input("Senha", type="password", key="l_s")
            if st.button("ENTRAR NO PAINEL"):
                try:
                    res = supabase.auth.sign_in_with_password({"email": e, "password": s})
                    st.session_state.user = res
                    st.rerun()
                except: st.error("Erro no login. Verifique os dados.")
        with tab_cad:
            e_c = st.text_input("Novo E-mail", key="c_e")
            s_c = st.text_input("Senha", type="password", key="c_s")
            if st.button("CRIAR CONTA"):
                try:
                    supabase.auth.sign_up({"email": e_c, "password": s_c})
                    st.success("Conta criada! Já pode logar.")
                except Exception as ex: st.error(f"Erro: {ex}")
else:
    # --- 6. INTERFACE PRINCIPAL TECHFOX ---
    with st.sidebar:
        st.markdown("<h2 style='color: #38bdf8;'>FOX CONTROL</h2>", unsafe_allow_html=True)
        nome_loja = st.text_input("Nome da sua Loja", "Fox Cell")
        whatsapp = st.text_input("Seu WhatsApp de Atendimento")
        st.divider()
        menu = st.radio("Selecione a Ferramenta:", [
            "📱 Post p/ Instagram", 
            "💬 Orçamento WhatsApp", 
            "📄 Ordem de Serviço (OS)"
        ])
        
        if st.button("Encerrar Sessão"):
            st.session_state.user = None
            st.rerun()

    # --- FERRAMENTA 1: POSTS ---
    if menu == "📱 Post p/ Instagram":
        st.title("🚀 Gerador de Conteúdo")
        st.markdown("Crie posts profissionais para atrair novos reparos.")
        
        with st.container():
            st.markdown('<div class="tech-card">', unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                aparelho = st.text_input("Qual o aparelho?", placeholder="Ex: iPhone 13 Pro Max")
                servico = st.selectbox("O que foi feito?", ["Troca de Tela", "Troca de Bateria", "Banho Químico", "Reparo de Placa", "Recuperação de FaceID"])
            with c2:
                tempo = st.text_input("Ficou pronto em quanto tempo?", "40 minutos")
                garantia = st.selectbox("Garantia dada", ["90 dias", "6 meses", "1 ano"])
            st.markdown('</div>', unsafe_allow_html=True)

        if st.button("GERAR LEGENDA Fox"):
            with st.spinner("IA analisando o reparo..."):
                model = get_model()
                prompt = (f"Crie um post para Instagram de assistência técnica de celular {nome_loja}. "
                          f"Fale sobre o reparo de {servico} no {aparelho}. "
                          f"Destaque que ficou pronto em {tempo} e tem {garantia} de garantia. "
                          f"Inclua emojis de tecnologia e hashtags relevantes.")
                res = model.generate_content(prompt)
                st.markdown(f'<div class="output-box">{res.text}</div>', unsafe_allow_html=True)
                copy_button(res.text, "post_fox")

    # --- FERRAMENTA 2: ORÇAMENTO ---
    elif menu == "💬 Orçamento WhatsApp":
        st.title("💰 Orçamento Profissional")
        st.markdown("Passe o preço com autoridade e feche mais serviços.")
        
        with st.container():
            st.markdown('<div class="tech-card">', unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                cliente = st.text_input("Nome do Cliente")
                modelo_cel = st.text_input("Aparelho do Cliente")
            with c2:
                valor_serv = st.text_input("Valor do Serviço (R$)")
                prazo_serv = st.text_input("Prazo de Entrega")
            defeito_rel = st.text_area("O que o aparelho tem?")
            st.markdown('</div>', unsafe_allow_html=True)

        if st.button("GERAR TEXTO PARA WHATSAPP"):
            model = get_model()
            prompt = (f"Atue como um técnico profissional da {nome_loja}. "
                      f"Gere uma mensagem para WhatsApp para o cliente {cliente} sobre o seu {modelo_cel}. "
                      f"O problema é {defeito_rel}. O valor é R$ {valor_serv} com entrega em {prazo_serv}. "
                      f"Seja educado e passe confiança técnica.")
            res = model.generate_content(prompt)
            st.markdown(f'<div class="output-box">{res.text}</div>', unsafe_allow_html=True)
            copy_button(res.text, "zap_fox")

    # --- FERRAMENTA 3: O.S. ---
    elif menu == "📄 Ordem de Serviço (OS)":
        st.title("📄 Registro de Entrada (O.S.)")
        st.info("Preencha os dados abaixo para gerar o resumo da entrada do aparelho.")
        
        with st.container():
            st.markdown('<div class="tech-card">', unsafe_allow_html=True)
            st.text_input("Nº da O.S. (Opcional)")
            st.text_input("IMEI ou Serial do Aparelho")
            st.text_area("Estado Físico (Ex: Tela trincada, marcas de uso na carcaça)")
            st.multiselect("Checklist de Entrada", ["Liga", "Carrega", "Câmeras OK", "Som OK", "Wi-Fi OK", "Botões OK"])
            st.markdown('</div>', unsafe_allow_html=True)
            
            if st.button("GERAR RESUMO DE ENTRADA"):
                st.warning("Próximo passo: Exportação em PDF será habilitada no plano Pro.")
