import streamlit as st
import google.generativeai as genai
import urllib.parse

# 1. إعداد الصفحة
st.set_page_config(page_title="Darija Ad Studio", page_icon="🎬", layout="wide")

# 2. الربط مع Gemini
if "GEMINI_API_KEY" not in st.secrets:
    st.error("Missing API Key in Secrets!")
else:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 3. اختيار الموديل أوتوماتيكياً (هنا فين كاين الحل)
@st.cache_resource
def get_working_model():
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    # غانختارو أول موديل فيه كلمة 'flash' ولا 'pro'
    for m in available_models:
        if 'flash' in m or 'pro' in m:
            return genai.GenerativeModel(m)
    return genai.GenerativeModel('gemini-pro') # الاحتياط

model = get_working_model()

# 4. الواجهة
st.title("🎬 Darija Cinematic Ad Studio")
user_input = st.sidebar.text_area("وصف فكرتك بالدارجة:", height=150)
generate_btn = st.sidebar.button("إطلاق الإبداع ✨")

if generate_btn and user_input:
    with st.spinner('⏳ جاري التحضير...'):
        try:
            prompt = f"Translate and expand this Darija concept: '{user_input}' into a professional Arabic ad script and provide an English cinematic image prompt. Format: SCRIPT: [text] IMAGE_PROMPT: [text]"
            response = model.generate_content(prompt)
            output = response.text
            
            if "IMAGE_PROMPT:" in output:
                parts = output.split("IMAGE_PROMPT:")
                script_part = parts[0].replace("SCRIPT:", "").strip()
                image_prompt = parts[1].strip()
            else:
                script_part, image_prompt = output, user_input

            col1, col2 = st.columns(2)
            with col1:
                st.subheader("📝 سكريبت الإعلان")
                st.success(script_part)
            with col2:
                st.subheader("🖼️ المشهد السينمائي")
                clean_p = urllib.parse.quote(image_prompt[:180])
                st.image(f"https://image.pollinations.ai/prompt/{clean_p}?width=1024&height=1024&nologo=true")
        except Exception as e:
            st.error(f"Error: {e}")
