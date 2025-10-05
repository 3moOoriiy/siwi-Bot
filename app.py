# app.py
# ============================================
# 🫒 خبير زيت الزيتون - AmrBot (Streamlit)
# ============================================

import google.generativeai as genai
import streamlit as st
import os

# ✅ إعدادات الصفحة
st.set_page_config(
    page_title="خبير زيت الزيتون 🫒",
    page_icon="🫒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ✅ الحصول على API Key بشكل آمن
# الطريقة 1: من متغيرات البيئة (الأفضل)
API_KEY = os.getenv("AIzaSyCXIirGg8Mf0j3gLqo3Sxs7kqgbSeHpovM")

# الطريقة 2: من Streamlit Secrets (للإنتاج)
if not API_KEY:
    try:
        API_KEY = st.secrets["GEMINI_API_KEY"]
    except:
        pass

# الطريقة 3: إدخال يدوي من المستخدم
if not API_KEY:
    st.sidebar.title("🔑 إعداد API Key")
    API_KEY = st.sidebar.text_input(
        "أدخل Gemini API Key:",
        type="password",
        help="احصل عليه من: https://makersuite.google.com/app/apikey"
    )
    if not API_KEY:
        st.error("⚠️ يرجى إدخال API Key للمتابعة!")
        st.info("📌 احصل على المفتاح من: https://makersuite.google.com/app/apikey")
        st.stop()

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

# ✅ CSS محسّن - تصميم احترافي وجذاب
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
    
    * {
        font-family: 'Cairo', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-attachment: fixed;
    }
    
    .stApp {
        background: transparent;
    }
    
    /* تحسين مربع المحادثة */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.95) !important;
        border-radius: 15px !important;
        padding: 15px 20px !important;
        margin: 10px 0 !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
        backdrop-filter: blur(10px);
    }
    
    /* تحسين رسائل المستخدم */
    [data-testid="stChatMessageContent"] {
        background: transparent !important;
    }
    
    /* تحسين Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2d3748 0%, #1a202c 100%) !important;
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* تحسين الأزرار */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6) !important;
    }
    
    /* تحسين مربع الإدخال */
    .stChatInputContainer {
        background: rgba(255, 255, 255, 0.95) !important;
        border-radius: 15px !important;
        padding: 10px !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.15) !important;
    }
    
    /* تحسين العنوان */
    h1 {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700 !important;
        text-align: center;
    }
    
    /* تحسين البطاقات */
    .stAlert {
        background: rgba(255, 255, 255, 0.9) !important;
        border-radius: 12px !important;
        border-left: 4px solid #667eea !important;
    }
    
    /* تحسين Metric */
    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.1) !important;
        padding: 15px !important;
        border-radius: 10px !important;
    }
    
    /* إخفاء عناصر streamlit الافتراضية */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# إعداد الاتصال بـ Google Gemini
try:
    genai.configure(api_key=API_KEY)
except Exception as e:
    st.error(f"❌ خطأ في تكوين API: {str(e)}")
    st.stop()

# ✅ تهيئة Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

if "model" not in st.session_state:
    try:
        st.session_state.model = genai.GenerativeModel("gemini-1.5-flash")
    except Exception as e:
        st.error(f"❌ خطأ في تحميل النموذج: {str(e)}")
        st.stop()

# ✅ دالة المحادثة
def get_gemini_response(user_message):
    try:
        chat_history = [{"role": "user", "parts": [SYSTEM_PROMPT]}]
        
        for msg in st.session_state.messages:
            role = "user" if msg["role"] == "user" else "model"
            chat_history.append({"role": role, "parts": [msg["content"]]})
        
        chat_history.append({"role": "user", "parts": [user_message]})
        
        response = st.session_state.model.generate_content(chat_history)
        return response.text
    
    except Exception as e:
        return f"❌ حدث خطأ: {str(e)}\n\n💡 تأكد من صحة API Key وأن لديك رصيد كافٍ"

# ✅ Sidebar المحسّنة
with st.sidebar:
    st.markdown("# 🫒 AmrBot")
    st.markdown("### خبيرك في زيت الزيتون")
    st.markdown("---")
    
    with st.expander("📚 عن البوت", expanded=True):
        st.markdown("""
        **مرحباً! أنا AmrBot** 👋
        
        خبير متخصص في كل ما يتعلق بزيت الزيتون
        
        **يمكنني مساعدتك في:**
        - 🌿 الفوائد الصحية
        - 🍳 وصفات الطبخ
        - 💆‍♀️ العناية بالبشرة والشعر
        - 🏆 اختيار الأفضل
        - 📦 التخزين السليم
        - 🔍 كشف الغش
        """)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ مسح", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    
    with col2:
        if st.button("🔄 إعادة", use_container_width=True):
            if len(st.session_state.messages) >= 2:
                last_user_msg = st.session_state.messages[-2]["content"]
                st.session_state.messages = st.session_state.messages[:-2]
                bot_response = get_gemini_response(last_user_msg)
                st.session_state.messages.append({"role": "user", "content": last_user_msg})
                st.session_state.messages.append({"role": "assistant", "content": bot_response})
                st.rerun()
    
    st.markdown("---")
    
    st.metric("💬 عدد الرسائل", len(st.session_state.messages))
    
    st.markdown("---")
    st.markdown("🔒 **خصوصية تامة**")
    st.caption("Made with ❤️ by AmrBot")

# ✅ الواجهة الرئيسية
st.title("🫒 AmrBot - خبير زيت الزيتون")
st.markdown("""
    <p style='text-align: center; font-size: 1.2em; color: white; background: rgba(255,255,255,0.1); 
    padding: 15px; border-radius: 10px; backdrop-filter: blur(10px);'>
    اسألني عن أي شيء متعلق بزيت الزيتون 🌿✨
    </p>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ✅ عرض أمثلة جميلة
if len(st.session_state.messages) == 0:
    st.markdown("""
        <div style='background: rgba(255,255,255,0.9); padding: 20px; border-radius: 15px; margin-bottom: 20px;'>
        <h3 style='text-align: center; color: #667eea;'>💡 أمثلة للبدء</h3>
        <p style='text-align: center; color: #666;'>اضغط على أي سؤال للبدء فوراً</p>
        </div>
        """, unsafe_allow_html=True)
    
    examples = [
        ("🌿", "ما هي فوائد زيت الزيتون الصحية؟"),
        ("🔍", "كيف أعرف زيت الزيتون الأصلي من المغشوش؟"),
        ("💆‍♀️", "هل زيت الزيتون مفيد للشعر؟"),
        ("⭐", "ما الفرق بين زيت الزيتون البكر الممتاز والعادي؟"),
        ("🍳", "كيف أستخدم زيت الزيتون في الطبخ؟"),
        ("⚖️", "هل زيت الزيتون يساعد في إنقاص الوزن؟"),
        ("📦", "ما أفضل طريقة لتخزين زيت الزيتون؟"),
        ("✨", "هل يمكن استخدام زيت الزيتون للبشرة؟")
    ]
    
    col1, col2 = st.columns(2)
    
    for i, (emoji, example) in enumerate(examples):
        col = col1 if i % 2 == 0 else col2
        if col.button(f"{emoji} {example}", key=f"ex_{i}", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": example})
            bot_response = get_gemini_response(example)
            st.session_state.messages.append({"role": "assistant", "content": bot_response})
            st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)

# ✅ عرض المحادثات
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="👤" if message["role"] == "user" else "🫒"):
        st.markdown(message["content"])

# ✅ مربع الإدخال
if prompt := st.chat_input("💬 اكتب سؤالك هنا عن زيت الزيتون..."):
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("assistant", avatar="🫒"):
        with st.spinner("🤔 جاري التفكير..."):
            response = get_gemini_response(prompt)
            st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
