import streamlit as st
import time
import random
from io import BytesIO

# --- 1. 核心相容性修復 ---
def safe_rerun():
    """自動判斷並執行重整"""
    try:
        st.rerun()
    except AttributeError:
        try:
            st.experimental_rerun()
        except:
            st.stop()

def safe_play_audio(text):
    """語音播放安全模式"""
    try:
        from gtts import gTTS
        # 使用印尼語 (id) 發音
        tts = gTTS(text=text, lang='id')
        fp = BytesIO()
        tts.write_to_fp(fp)
        st.audio(fp, format='audio/mp3')
    except Exception as e:
        st.caption(f"🔇 (語音生成暫時無法使用)")

# --- 0. 系統配置 ---
st.set_page_config(page_title="Unit 14: O Romi'ad", page_icon="🌦️", layout="centered")

# --- CSS 美化 ---
st.markdown("""
    <style>
    body { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    .source-tag { font-size: 12px; color: #aaa; text-align: right; font-style: italic; }
    
    /* 單字卡 - 天空藍漸層 */
    .word-card {
        background: linear-gradient(135deg, #E3F2FD 0%, #ffffff 100%);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 15px;
        border-bottom: 4px solid #2196F3;
    }
    .emoji-icon { font-size: 48px; margin-bottom: 10px; }
    .amis-text { font-size: 22px; font-weight: bold; color: #1565C0; }
    .chinese-text { font-size: 16px; color: #7f8c8d; }
    
    /* 句子框 */
    .sentence-box {
        background-color: #E1F5FE;
        border-left: 5px solid #039BE5;
        padding: 15px;
        margin: 10px 0;
        border-radius: 0 10px 10px 0;
    }

    /* 按鈕 */
    .stButton>button {
        width: 100%; border-radius: 12px; font-size: 20px; font-weight: 600;
        background-color: #B3E5FC; color: #0277BD; border: 2px solid #29B6F6; padding: 12px;
    }
    .stButton>button:hover { background-color: #81D4FA; border-color: #039BE5; }
    .stProgress > div > div > div > div { background-color: #03A9F4; }
    </style>
""", unsafe_allow_html=True)

# --- 2. 資料庫 (Unit 14 最終修正) ---
vocab_data = [
    {"amis": "Romi'ad", "chi": "天氣 / 日子", "icon": "📅", "source": "Row 255"},
    {"amis": "Cidal", "chi": "太陽", "icon": "☀️", "source": "Basic"},
    {"amis": "'Orad", "chi": "雨 / 雨水", "icon": "🌧️", "source": "User Fix"},
    {"amis": "Fali", "chi": "風", "icon": "🍃", "source": "Basic"},
    {"amis": "Folad", "chi": "月亮", "icon": "🌙", "source": "Basic"},
    {"amis": "Fo'is", "chi": "星星", "icon": "⭐", "source": "Basic"},
    {"amis": "Kakarayan", "chi": "天空", "icon": "🌌", "source": "Basic"},
    {"amis": "Si'enaw", "chi": "冷 (天氣)", "icon": "🥶", "source": "Row 255"},
    {"amis": "Fa^edet", "chi": "熱 / 熱度", "icon": "🥵", "source": "Row 538 (Fix)"},
    {"amis": "Anini", "chi": "今天 / 現在", "icon": "👇", "source": "Basic"},
]

sentences = [
    {"amis": "Si'enaw ko romi'ad.", "chi": "天氣很冷。", "icon": "🥶", "source": "Row 255"},
    {"amis": "Ma'orad anini.", "chi": "今天下雨。", "icon": "🌧️", "source": "User Fix"}, # 修正拼寫
    {"amis": "Fa^edet ko cidal.", "chi": "太陽很熱。", "icon": "☀️", "source": "User Fix"},
    {"amis": "I kakarayan ko fo'is.", "chi": "星星在天空。", "icon": "⭐", "source": "Unit 13"},
    {"amis": "Tata'ang ko fali.", "chi": "風很大。", "icon": "🍃", "source": "Tata'ang (大)"},
]

# --- 3. 隨機題庫 ---
quiz_pool = [
    {
        "q": "Si'enaw ko romi'ad.",
        "audio": "Si'enaw ko romi'ad",
        "options": ["天氣很冷", "天氣很熱", "今天下雨"],
        "ans": "天氣很冷",
        "hint": "Si'enaw 是冷"
    },
    {
        "q": "O maan ko i kakarayan? (天上有什麼？)",
        "audio": "O maan ko i kakarayan",
        "options": ["O fo'is (星星)", "O foting (魚)", "O waco (狗)"],
        "ans": "O fo'is (星星)",
        "hint": "Kakarayan 是天空"
    },
    {
        "q": "Ma'orad anini.",
        "audio": "Ma'orad anini",
        "options": ["今天下雨", "今天很熱", "今天去台東"],
        "ans": "今天下雨",
        "hint": "'Orad 是雨，Ma'orad 是下雨"
    },
    {
        "q": "單字測驗：Cidal",
        "audio": "Cidal",
        "options": ["太陽", "月亮", "星星"],
        "ans": "太陽",
        "hint": "白天出現的"
    },
    {
        "q": "單字測驗：Fali",
        "audio": "Fali",
        "options": ["風", "雨", "雲"],
        "ans": "風",
        "hint": "看不見但吹起來涼涼的"
    },
    {
        "q": "Fa^edet ko cidal.",
        "audio": "Fa^edet ko cidal",
        "options": ["太陽很熱", "月亮很亮", "星星很多"],
        "ans": "太陽很熱",
        "hint": "Fa^edet 是熱"
    },
    {
        "q": "你要怎麼說「天氣」或「日子」？",
        "audio": None,
        "options": ["Romi'ad", "Hekal", "Loma'"],
        "ans": "Romi'ad",
        "hint": "Si'enaw ko..."
    }
]

# --- 4. 狀態初始化 ---
if 'init' not in st.session_state:
    st.session_state.score = 0
    st.session_state.quiz_questions = random.sample(quiz_pool, 3)
    st.session_state.current_q_idx = 0
    st.session_state.quiz_id = str(random.randint(1000, 9999))
    st.session_state.init = True

# --- 5. 主介面 ---
st.markdown("<h1 style='text-align: center; color: #0277BD;'>Unit 14: O Romi'ad</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>天氣與自然</p>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📚 詞彙與句型", "🎲 隨機挑戰"])

# === Tab 1: 學習模式 ===
with tab1:
    st.subheader("📝 核心單字")
    col1, col2 = st.columns(2)
    for i, word in enumerate(vocab_data):
        with (col1 if i % 2 == 0 else col2):
            st.markdown(f"""
            <div class="word-card">
                <div class="emoji-icon">{word['icon']}</div>
                <div class="amis-text">{word['amis']}</div>
                <div class="chinese-text">{word['chi']}</div>
                <div class="source-tag">src: {word['source']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"🔊 聽發音", key=f"btn_vocab_{i}"):
                safe_play_audio(word['amis'])

    st.markdown("---")
    st.subheader("🗣️ 實用句型")
    for i, s in enumerate(sentences):
        st.markdown(f"""
        <div class="sentence-box">
            <div style="font-size: 20px; font-weight: bold; color: #01579B;">{s['icon']} {s['amis']}</div>
            <div style="font-size: 16px; color: #555; margin-top: 5px;">{s['chi']}</div>
            <div class="source-tag">src: {s['source']}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"▶️ 播放句型", key=f"btn_sent_{i}"):
            safe_play_audio(s['amis'])

# === Tab 2: 隨機挑戰模式 ===
with tab2:
    st.markdown("### 🎲 隨機評量")
    
    if st.session_state.current_q_idx < len(st.session_state.quiz_questions):
        q_data = st.session_state.quiz_questions[st.session_state.current_q_idx]
        
        st.progress((st.session_state.current_q_idx) / 3)
        st.markdown(f"**Question {st.session_state.current_q_idx + 1} / 3**")
        
        st.markdown(f"### {q_data['q']}")
        if q_data['audio']:
            if st.button("🎧 播放題目音檔", key=f"btn_audio_{st.session_state.current_q_idx}"):
                safe_play_audio(q_data['audio'])
        
        unique_key = f"q_{st.session_state.quiz_id}_{st.session_state.current_q_idx}"
        user_choice = st.radio("請選擇正確答案：", q_data['options'], key=unique_key)
        
        if st.button("送出答案", key=f"btn_submit_{st.session_state.current_q_idx}"):
            if user_choice == q_data['ans']:
                st.balloons()
                st.success("🎉 答對了！")
                time.sleep(1)
                st.session_state.score += 100
                st.session_state.current_q_idx += 1
                safe_rerun()
            else:
                st.error(f"不對喔！提示：{q_data['hint']}")
                
    else:
        st.progress(1.0)
        st.markdown(f"""
        <div style='text-align: center; padding: 30px; background-color: #B3E5FC; border-radius: 20px; margin-top: 20px;'>
            <h1 style='color: #01579B;'>🏆 挑戰成功！</h1>
            <h3 style='color: #333;'>本次得分：{st.session_state.score}</h3>
            <p>你已經學會看天氣了！</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 再來一局 (重新抽題)", key="btn_restart"):
            st.session_state.score = 0
            st.session_state.current_q_idx = 0
            st.session_state.quiz_questions = random.sample(quiz_pool, 3)
            st.session_state.quiz_id = str(random.randint(1000, 9999))
            safe_rerun()

