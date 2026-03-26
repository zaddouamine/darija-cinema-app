import streamlit as st
import google.generativeai as genai
import re
import urllib.parse

# 1. إعداد الصفحة
st.set_page_config(page_title="Darija Ad Studio", page_icon="🎬", layout="wide")

# 2. الربط مع Gemini
if "GEMINI_API_KEY" not in st.secrets:
    st.error("Missing API Key in Secrets!")
else:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

@st.cache_resource
def get_working_model():
    # كيجرب يلقى الموديل اللي خدام عندك
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    for m in available_models:
        if 'flash' in m or 'pro' in m:
            return genai.GenerativeModel(m)
    return genai.GenerativeModel('gemini-1.5-flash-latest')

model = get_working_model()

# 3. الواجهة
st.title("🎬 Darija Cinematic Ad Studio")
st.markdown("---")

user_input = st.sidebar.text_area("وصف فكرتك بالدارجة:", height=150)
generate_btn = st.sidebar.button("إطلاق الإبداع ✨")

if generate_btn and user_input:
    with st.spinner('⏳ جاري التحضير...'):
        try:
            # طلب السكريبت والوصف بطريقة نقية
            prompt = f"Create a professional Arabic ad script for: '{user_input}'. After the script, write only 'IMAGE_PROMPT: ' and a short English cinematic description. NO BOLD STARS **."
            response = model.generate_content(prompt)
            output = response.text
            
            if "IMAGE_PROMPT:" in output:
                script_part = output.split("IMAGE_PROMPT:")[0].strip()
                image_desc = output.split("IMAGE_PROMPT:")[1].strip()
            else:
                script_part, image_desc = output, user_input

            # تنظيف الوصف من الرموز (هنا السر)
            clean_desc = re.sub(r'[^a-zA-Z0-9\s]', '', image_desc)
            encoded_desc = urllib.parse.quote(clean_desc)
            
            # رابط الصورة
            image_url = f"https://image.pollinations.ai/prompt/{encoded_desc}?width=1024&height=1024&nologo=true"

            col1, col2 = st.columns(2)
            with col1:
                st.subheader("📝 سكريبت الإعلان")
                st.info(script_part)
            with col2:
                st.subheader("🖼️ المشهد السينمائي")
                st.image(image_url, use_container_width=True)

        except Exception as e:
            st.error(f"Error: {e}")
