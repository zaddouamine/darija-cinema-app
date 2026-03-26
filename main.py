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

# 3. اختيار الموديل أوتوماتيكياً
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
st.markdown("---") # خط فاصل

# خانة الكتابة على اليسار
user_input = st.sidebar.text_area("وصف فكرتك بالدارجة:", height=150)
generate_btn = st.sidebar.button("إطلاق الإبداع ✨")

if generate_btn and user_input:
    with st.spinner('⏳ جاري التحضير...'):
        try:
            # طلب السكريبت فقط من Gemini (باش يركز)
            script_prompt = f"Expand this Darija concept: '{user_input}' into a professional Arabic or Darija cinematic ad script."
            script_response = model.generate_content(script_prompt)
            script_part = script_response.text

            # طلب الـ Image Prompt فقط من Gemini (باش ما يضيعش الوقت)
            # إيلا Gemini تلطل فـ السكريبت، غانخدمو بـ user_input مباشرة كـ Image Prompt
            try:
                # طلب Description دقيقة للمشهد بالنكليزية
                image_desc_prompt = f"Create a short, cinematic English image prompt that perfectly describes the main visual concept from this Darija description: '{user_input}'."
                image_desc_response = model.generate_content(image_desc_prompt)
                image_prompt = image_desc_response.text
            except Exception:
                # إيلا تعطل Gemini، خدمو بوصف فكرتك مباشرة كـ Image Prompt (باش ما نضيعوش التصويرة)
                image_prompt = user_input

            # العرض
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("📝 سكريبت الإعلان")
                # إيلا طلع السكريبت مكتوب بـ Markdown كبيير، غانخلوه عادي
                st.info(script_part)
            with col2:
                st.subheader("🖼️ المشهد السينمائي")
                
                # تنظيف وتنصيب Image Prompt
                clean_p = urllib.parse.quote(image_prompt[:250]) # زدنا شوية فـ الطول
                image_url = f"https://image.pollinations.ai/prompt/{clean_p}?width=1024&height=1024&nologo=true&seed=42"
                
                # عرض التصويرة
                st.image(image_url, use_container_width=True)

        except Exception as e:
            st.error(f"Error: {e}")
