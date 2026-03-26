import streamlit as st
import google.generativeai as genai
import urllib.parse

# 1. إعداد الصفحة
st.set_page_config(page_title="Darija Ad Studio", page_icon="🎬", layout="wide")

# 2. الربط مع Gemini
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except:
    st.error("Missing API Key in Secrets!")

model = genai.GenerativeModel('gemini-1.5-flash')

# 3. الواجهة
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
                script_part = output.split("IMAGE_PROMPT:")[0].replace("SCRIPT:", "").strip()
                image_prompt = output.split("IMAGE_PROMPT:")[1].strip()
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

