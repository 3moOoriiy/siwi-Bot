# app.py
# ============================================
# 🫒 خبير زيت الزيتون - AmrBot (Streamlit)
# ============================================

import google.generativeai as genai
import streamlit as st

# ✅ إعدادات الصفحة
st.set_page_config(
    page_title="خبير زيت الزيتون 🫒",
    page_icon="🫒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ✅ ضع هنا مفتاح Gemini API الخاص بك
API_KEY = "AIzaSyCXIirGg8Mf0j3gLqo3Sxs7kqgbSeHpovM"  

# ✅ System Prompt - شخصية البوت المتخصصة
SYSTEM_PROMPT = """أنت خبير متخصص في زيت الزيتون اسمك "AmrBot". 
لديك معرفة عميقة بكل ما يتعلق بزيت الزيتون:
- أنواع زيت الزيتون (البكر الممتاز، البكر، المكرر، إلخ)
- الفوائد الصحية والغذائية
- طرق الاستخدام في الطبخ والعناية بالبشرة والشعر
- كيفية اختيار زيت زيتون عالي الجودة
- التخزين الصحيح والصلاحية
- الفرق بين الأنواع المختلفة والأسعار
- الاستخدامات العلاجية والطبية
- تاريخ زيت الزيتون وزراعته
- الدول المنتجة والأنواع المشهورة

تحدث بأسلوب ودود وخبير. اشرح بطريقة سهلة ومفصلة. 
إذا سألك أحد عن شيء خارج نطاق زيت الزيتون، وجهه بلطف للحديث عن زيت الزيتون.
استخدم الرموز التعبيرية المناسبة 🫒✨"""

# ✅ CSS مخصص للتنسيق
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.8);
        border-radius: 10px;
        padding: 10px;
        margin: 5px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# ✅ التحقق من API Key
if not API_KEY:
    st.error("⚠️ يرجى إضافة API_KEY في السطر 16 من الكود!")
    st.info("احصل على المفتاح من: https://makersuite.google.com/app/apikey")
    st.stop()

# إعداد الاتصال بـ Google Gemini
genai.configure(api_key=API_KEY)

# ✅ تهيئة Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

if "model" not in st.session_state:
    st.session_state.model = genai.GenerativeModel("gemini-1.5-flash")

# ✅ دالة المحادثة
def get_gemini_response(user_message):
    try:
        # بناء المحادثة مع System Prompt
        chat_history = [{"role": "user", "parts": [SYSTEM_PROMPT]}]
        
        # إضافة سجل المحادثات
        for msg in st.session_state.messages:
            role = "user" if msg["role"] == "user" else "model"
            chat_history.append({"role": role, "parts": [msg["content"]]})
        
        # إضافة الرسالة الحالية
        chat_history.append({"role": "user", "parts": [user_message]})
        
        # الحصول على الرد
        response = st.session_state.model.generate_content(chat_history)
        return response.text
    
    except Exception as e:
        return f"❌ حدث خطأ: {str(e)}"

# ✅ Sidebar - القائمة الجانبية
with st.sidebar:
    st.title("🫒 خبير زيت الزيتون")
    st.markdown("---")
    
    # معلومات البوت
    st.markdown("""
    ### 👋 مرحباً بك!
    أنا **AmrBot**، خبيرك الشخصي في زيت الزيتون.
    
    **اسألني عن:**
    - 🌿 فوائد زيت الزيتون
    - 🍳 استخدامات الطبخ
    - 💆‍♀️ العناية بالبشرة والشعر
    - 🏆 أفضل الأنواع والجودة
    - 📦 التخزين والصلاحية
    - 🔍 التمييز بين الأصلي والمغشوش
    """)
    
    st.markdown("---")
    
    # أزرار التحكم
    if st.button("🗑️ مسح المحادثة", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    if st.button("🔄 إعادة آخر رسالة", use_container_width=True):
        if len(st.session_state.messages) >= 2:
            last_user_msg = st.session_state.messages[-2]["content"]
            st.session_state.messages = st.session_state.messages[:-2]
            
            # إعادة إرسال الرسالة
            bot_response = get_gemini_response(last_user_msg)
            st.session_state.messages.append({"role": "user", "content": last_user_msg})
            st.session_state.messages.append({"role": "assistant", "content": bot_response})
            st.rerun()
    
    st.markdown("---")
    
    # إحصائيات المحادثة
    st.metric("عدد الرسائل", len(st.session_state.messages))
    
    st.markdown("---")
    st.caption("Made with ❤️ by AmrBot")

# ✅ الواجهة الرئيسية
st.title("🫒 AmrBot - خبيرك الشخصي في زيت الزيتون")
st.markdown("### اسأل عن أي شيء متعلق بزيت الزيتون: فوائده، استخداماته، أنواعه، وأكثر!")
st.markdown("---")

# ✅ عرض أمثلة للبدء (إذا كانت المحادثة فارغة)
if len(st.session_state.messages) == 0:
    st.info("👇 اضغط على أي سؤال من الأمثلة أدناه للبدء:")
    
    col1, col2 = st.columns(2)
    
    examples = [
        "ما هي فوائد زيت الزيتون الصحية؟",
        "كيف أعرف زيت الزيتون الأصلي من المغشوش؟",
        "هل زيت الزيتون مفيد للشعر؟",
        "ما الفرق بين زيت الزيتون البكر الممتاز والعادي؟",
        "كيف أستخدم زيت الزيتون في الطبخ؟",
        "هل زيت الزيتون يساعد في إنقاص الوزن؟",
        "ما أفضل طريقة لتخزين زيت الزيتون؟",
        "هل يمكن استخدام زيت الزيتون للبشرة؟"
    ]
    
    for i, example in enumerate(examples):
        col = col1 if i % 2 == 0 else col2
        if col.button(f"💬 {example}", key=f"example_{i}", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": example})
            bot_response = get_gemini_response(example)
            st.session_state.messages.append({"role": "assistant", "content": bot_response})
            st.rerun()

# ✅ عرض المحادثات
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="👤" if message["role"] == "user" else "🫒"):
        st.markdown(message["content"])

# ✅ مربع إدخال الرسالة
if prompt := st.chat_input("اسألني عن زيت الزيتون... 🫒"):
    # عرض رسالة المستخدم
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # الحصول على رد البوت
    with st.chat_message("assistant", avatar="🫒"):
        with st.spinner("جاري التفكير... 🤔"):
            response = get_gemini_response(prompt)
            st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
