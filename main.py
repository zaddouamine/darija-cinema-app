import streamlit as st
import google.generativeai as genai
import re
import urllib.parse

st.set_page_config(page_title="Darija Ad Studio", page_icon="🎬", layout="wide")

if "GEMINI_API_KEY" not in st.secrets:
    st.error("Missing API Key in Secrets!")
else:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

@st.cache_resource
def get_working_model():
    try:
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        for m in models:
            if 'flash' in m or 'pro' in m: return genai.GenerativeModel(m)
    except: pass
    return genai.GenerativeModel('gemini-1.5-flash-latest')

model = get_working_model()

st.title("🎬 Darija Cinematic Ad Studio")
st.markdown("---")

user_input = st.sidebar.text_area("وصف فكرتك بالدارجة:", height=150)
generate_btn = st.sidebar.button("إطلاق الإبداع ✨")

if generate_btn and user_input:
    with st.spinner('⏳ جاري التحضير...'):
        try:
            res = model.generate_content(f"Create a professional Arabic ad script for: {user_input}. Then write 'IMAGE_PROMPT: ' and 3 English keywords only.")
            text = res.text
            
            if "IMAGE_PROMPT:" in text:
                script_part = text.split("IMAGE_PROMPT:")[0]
                image_desc = text.split("IMAGE_PROMPT:")[1]
            else:
                script_part, image_desc = text, user_input

            clean_desc = re.sub(r'[^a-zA-Z\s]', '', image_desc).strip()
            # استعملنا هاد السيرفور حيت كيبان عند كولشي
            final_image_url = f"https://loremflickr.com/1024/1024/{urllib.parse.quote(clean_desc)}"

            col1, col2 = st.columns(2)
            with col1:
                st.subheader("📝 سكريبت الإعلان")
                st.info(script_part)
            with col2:
                st.subheader("🖼️ المشهد السينمائي")
                st.image(final_image_url, use_container_width=True)

        except Exception as e:
            st.error(f"Error: {e}")
