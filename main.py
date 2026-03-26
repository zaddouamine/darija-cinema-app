import streamlit as st
import google.generativeai as genai
import urllib.parse

# 1. إعداد الصفحة والتصميم (Luxury Dark Theme)
st.set_page_config(page_title="Darija Cinematic Ad Studio", page_icon="🎬", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stButton>button { 
        width: 100%; 
        border-radius: 20px; 
        background: linear-gradient(45deg, #ff4b4b, #ff7517); 
        color: white; 
        font-weight: bold;
        border: none; 
        padding: 10px;
    }
    .stTextArea>div>div>textarea { background-color: #262730; color: white; border-radius: 10px; }
    .img-container { border: 3px solid #333; border-radius: 15px; overflow: hidden; margin-top: 20px; box-shadow: 0px 10px 30px rgba(0,0,0,0.5); }
    h1, h3 { color: #ff4b4b; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# 2. جلب الساروت من Secrets (فـ Streamlit Cloud كيتسماو Secrets)
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except:
    st.warning("⚠️ خاصك تزيد GEMINI_API_KEY في Advanced Settings ديال Streamlit!")

model = genai.GenerativeModel('gemini-1.5-flash')

st.title("🎬 Darija Cinematic Ad Studio")
st.markdown("<h3 style='text-align: center; color: white;'>صاوب إعلان احترافي بالدارجة فـ ثواني</h3>", unsafe_allow_html=True)

# 3. واجهة المستخدم (Sidebar)
with st.sidebar:
    st.header("⚙️ الإعدادات")
    user_input = st.text_area("وصف فكرتك بالدارجة:", placeholder="مثلاً: بطل مغربي لابس جلبابة كيشوف فصومعة حسان وقت الغروب...", height=150)
    generate_btn = st.button("إطلاق الإبداع ✨")
    st.markdown("---")
    st.caption("Powered by Gemini 1.5 & Pollinations AI")

# 4. معالجة الطلب
if generate_btn and user_input:
    with st.spinner('⏳ جاري تحليل الدارجة وصناعة المشهد...'):
        try:
            # طلب السكريبت والوصف من Gemini
            prompt = f"""
            You are a creative ad director. 
            1. Translate and expand this Darija concept: '{user_input}' into a professional 30-second Arabic ad script. 
            2. Provide a separate HIGHLY DETAILED cinematic image prompt in English for the main scene.
            
            Format your response exactly like this:
            SCRIPT: [The Arabic/Darija Script]
            IMAGE_PROMPT: [The English Cinematic Prompt]
            """
            
            response = model.generate_content(prompt)
            output = response.text
            
            # تقسيم النص للسكريبت والوصف
            if "IMAGE_PROMPT:" in output:
                script_part = output.split("IMAGE_PROMPT:")[0].replace("SCRIPT:", "").strip()
                image_prompt = output.split("IMAGE_PROMPT:")[1].strip()
            else:
                script_part = output
                image_prompt = user_input

            # عرض النتائج في أعمدة
            col1, col2 = st.columns(
