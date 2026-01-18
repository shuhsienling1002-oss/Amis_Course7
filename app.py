import streamlit as st
import time
import os
from gtts import gTTS
from io import BytesIO

# --- 0. 系統配置 ---
st.set_page_config(page_title="Unit 7: O hekal", page_icon="🏔️", layout="centered")

# CSS 優化
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        font-size: 24px;
        background-color: #FFD700;
        color: #333;
        border: none;
        padding: 10px;
        margin-top: 10px;
    }
    .stButton>button:hover {
        background-color: #FFC107;
        transform: scale(1.02);
    }
    .big-font {
        font-size: 40px !important;
        font-weight: bold;
        color: #2E86C1;
        text-align: center;
        margin-bottom: 5px;
    }
    .med-font {
        font-size: 22px !important;
        color: #555;
        text-align: center;
        margin-bottom: 10px;
    }
    .card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 1. 數據資料庫 (Unit 7 專屬) ---

# 單字：大自然 (全部小寫)
VOCABULARY = {
    "cidal":    {"zh": "太陽", "emoji": "☀️", "file": "u7_cidal"},
    "folad":    {"zh": "月亮", "emoji": "🌙", "file": "u7_folad"},
    "fo'is":    {"zh": "星星", "emoji": "⭐", "file": "u7_fois"},
    "lotok":    {"zh": "山", "emoji": "⛰️", "file": "u7_lotok"},
    "riyar":    {"zh": "海", "emoji": "🌊", "file": "u7_riyar"},
    "kilang":   {"zh": "樹", "emoji": "🌳", "file": "u7_kilang"}
}

# 句型：描述與存在
SENTENCES = [
    {"amis": "Ira ko cidal.", "zh": "有太陽 (天氣晴)。", "file": "u7_s_sun_is_out"},
    {"amis": "Fangcal ko riyar.", "zh": "海很漂亮。", "file": "u7_s_beautiful_sea"},
    {"amis": "O maan koni?", "zh": "這是什麼？", "file": "u7_q_what"}
]

# --- 1.5 智慧語音核心 ---
def play_audio(text, filename_base=None):
    if filename_base:
        path_m4a = f"audio/{filename_base}.m4a"
        if os.path.exists(path_m4a):
            st.audio(path_m4a, format='audio/mp4')
            return
        path_mp3 = f"audio/{filename_base}.mp3"
        if os.path.exists(path_mp3):
            st.audio(path_mp3, format='audio/mp3')
            return

    try:
        # 使用印尼語 (id) 模擬南島語系發音
        tts = gTTS(text=text, lang='id')
        fp = BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        st.audio(fp, format='audio/mp3')
    except:
        st.caption("🔇 (無聲)")

# --- 2. 狀態管理 ---
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'current_q' not in st.session_state:
    st.session_state.current_q = 0

# --- 3. 學習模式 ---
def show_learning_mode():
    # 修正標題拼寫：Sakapito
    st.markdown("<h2 style='text-align: center;'>Sakapito: O hekal</h2>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: gray;'>美麗的大自然 🏔️</h4>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    words = list(VOCABULARY.items())
    
    for idx, (amis, data) in enumerate(words):
        with (col1 if idx % 2 == 0 else col2):
            with st.container():
                st.markdown(f"""
                <div class="card">
                    <div style="font-size: 60px;">{data['emoji']}</div>
                    <div class="big-font">{amis}</div>
                    <div class="med-font">{data['zh']}</div>
                </div>
                """, unsafe_allow_html=True)
                play_audio(amis, filename_base=data.get('file'))

    st.markdown("---")
    st.markdown("### 🗣️ 句型練習")
    
    # 存在句
    st.markdown("#### ☀️ 天氣/存在")
    s1 = SENTENCES[0]
    st.info(f"🔹 {s1['amis']} ({s1['zh']})")
    play_audio(s1['amis'], filename_base=s1.get('file'))
    
    # 形容詞句
    st.markdown("#### ✨ 讚美")
    s2 = SENTENCES[1]
    st.warning(f"🔹 {s2['amis']} ({s2['zh']})")
    play_audio(s2['amis'], filename_base=s2.get('file'))

# --- 4. 測驗模式 ---
def show_quiz_mode():
    # 修正標題拼寫：Sakapito
    st.markdown("<h2 style='text-align: center;'>🎮 Sakapito 小小探險家</h2>", unsafe_allow_html=True)
    progress = st.progress(st.session_state.current_q / 3)
    
    # 第一關：聽音辨位
    if st.session_state.current_q == 0:
        st.markdown("### 第一關：這是什麼聲音？")
        st.write("請聽單字：")
        play_audio("riyar", filename_base="u7_riyar")
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🌊 riyar (海)"):
                st.balloons()
                st.success("答對了！ Riyar 是海！")
                time.sleep(1)
                st.session_state.score += 100
                st.session_state.current_q += 1
                st.rerun()
        with c2:
            if st.button("⛰️ lotok (山)"): st.error("不對喔，lotok 是山！")

    # 第二關：句子理解
    elif st.session_state.current_q == 1:
        st.markdown("### 第二關：哪裡很漂亮？")
        st.markdown("#### 請聽句子：")
        play_audio("Fangcal ko riyar.", filename_base="u7_s_beautiful_sea")
        
        st.write("請問句子說什麼很漂亮？")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🌊 大海"):
                st.snow()
                st.success("沒錯！ Fangcal ko riyar.")
                time.sleep(1)
                st.session_state.score += 100
                st.session_state.current_q += 1
                st.rerun()
        with c2:
            if st.button("☀️ 太陽"): st.error("不對喔！")

    # 第三關：看圖問答
    elif st.session_state.current_q == 2:
        st.markdown("### 第三關：看圖回答")
        st.markdown("#### Q: O maan koni? (這是什麼？)")
        play_audio("O maan koni?", filename_base="u7_q_what") 
        
        st.markdown("<div style='font-size:80px; text-align:center;'>🌙</div>", unsafe_allow_html=True)
        
        options = ["O folad (是月亮)", "O cidal (是太陽)", "O fo'is (是星星)"]
        choice = st.radio("請選擇：", options)
        
        if st.button("確定送出"):
            if "folad" in choice:
                st.balloons()
                st.success("太厲害了！全部答對！")
                time.sleep(1)
                st.session_state.score += 100
                st.session_state.current_q += 1
                st.rerun()
            else:
                st.error("再看一次圖片喔！")

    else:
        st.markdown(f"<div style='text-align: center;'><h1>🏆 挑戰完成！</h1><h2>得分：{st.session_state.score}</h2></div>", unsafe_allow_html=True)
        if st.button("再玩一次"):
            st.session_state.current_q = 0
            st.session_state.score = 0
            st.rerun()

# --- 5. 主程式入口 ---
st.sidebar.title("Unit 7: O hekal 🏔️")
mode = st.sidebar.radio("選擇模式", ["📖 學習單詞", "🎮 練習挑戰"])

if mode == "📖 學習單詞":
    show_learning_mode()
else:
    show_quiz_mode()
