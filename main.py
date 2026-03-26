import streamlit as st
import google.generativeai as genai
import re

# 1. إعداد الصفحة
st.set_page_config(page_title="Darija Ad Studio", page_icon="🎬", layout="wide")

# 2. الربط مع Gemini
if "GEMINI_API_KEY" not in st.secrets:
    st.error("Missing API Key in Secrets!")
else:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

@st.cache_resource
def get_working_model():
    try:
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        for m in available_models:
            if 'flash' in m or 'pro' in m:
                return genai.GenerativeModel(m)
    except:
        pass
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
            # طلب السكريبت والوصف
            full_prompt = f"Create a professional Arabic ad script for: '{user_input}'. Also, at the very end, write 'IMAGE_PROMPT: ' followed by a short English cinematic description of the main scene. No bold markers like ** please."
            response = model.generate_content(full_prompt)
            output = response.text
            
            # استخراج السكريبت ووصف الصورة
            if "IMAGE_PROMPT:" in output:
                script_part = output.split("IMAGE_PROMPT:")[0].strip()
                image_desc = output.split("IMAGE_PROMPT:")[1].strip()
            else:
                script_part = output
                image_desc = user_input

            # تنظيف وصف الصورة من أي رموز خايبة (المهم جداً)
            clean_description = re.sub(r'[^a-zA-Z0-9\s]', '', image_desc)
            image_url = f"https://image.pollinations.ai/prompt/{clean_description.replace(' ', '%20')}?width=1024&height=1024&nologo=true"

            col1, col2 = st.columns(2)
            with col1:
                st.subheader("📝 سكريبت الإعلان")
                st.info(script_part)
            with col2:
                st.subheader("🖼️ المشهد السينمائي")
                st.image(image_url, use_container_width=True, caption="تصويرة ذكية لفكرتك")

        except Exception as e:
            st.error(f"وقع مشكل صغيور: {e}")
