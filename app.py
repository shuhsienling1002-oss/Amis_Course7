import streamlit as st
import time
import os
from gtts import gTTS
from io import BytesIO

# --- 0. 系統配置 ---
st.set_page_config(page_title="Unit 6: O kakaenen", page_icon="🍌", layout="centered")

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

# --- 1. 數據資料庫 (Unit 6 專屬) ---

# 單字：食物 (全部小寫)
VOCABULARY = {
    "hemay":    {"zh": "飯", "emoji": "🍚", "file": "u6_hemay"},
    "nanom":    {"zh": "水", "emoji": "💧", "file": "u6_nanom"},
    "pawli":    {"zh": "香蕉", "emoji": "🍌", "file": "u6_pawli"},
    "konga":    {"zh": "地瓜", "emoji": "🍠", "file": "u6_konga"},
    "dateng":   {"zh": "菜/蔬菜", "emoji": "🥬", "file": "u6_dateng"},
    "mami'":    {"zh": "橘子/柑橘", "emoji": "🍊", "file": "u6_mami"}
}

# 句型：喜好與動作
SENTENCES = [
    {"amis": "Maolah kako to pawli.", "zh": "我喜歡香蕉。", "file": "u6_s_like_banana"},
    {"amis": "Komaen to konga.", "zh": "在吃地瓜。", "file": "u6_s_eat_sweetpotato"},
    {"amis": "O maan koni?", "zh": "這是什麼？", "file": "u6_q_what"}
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
    # 修正標題拼寫：Saka'enem
    st.markdown("<h2 style='text-align: center;'>Saka'enem: O kakaenen</h2>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: gray;'>好吃的食物 😋</h4>", unsafe_allow_html=True)
    
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
    
    # 喜好
    st.markdown("#### ❤️ 表達喜歡")
    s1 = SENTENCES[0]
    st.info(f"🔹 {s1['amis']} ({s1['zh']})")
    play_audio(s1['amis'], filename_base=s1.get('file'))
    
    # 動作
    st.markdown("#### 🍽️ 正在吃...")
    s2 = SENTENCES[1]
    st.warning(f"🔹 {s2['amis']} ({s2['zh']})")
    play_audio(s2['amis'], filename_base=s2.get('file'))

# --- 4. 測驗模式 ---
def show_quiz_mode():
    # 修正標題拼寫：Saka'enem
    st.markdown("<h2 style='text-align: center;'>🎮 Saka'enem 美食家</h2>", unsafe_allow_html=True)
    progress = st.progress(st.session_state.current_q / 3)
    
    # 第一關：聽音辨位
    if st.session_state.current_q == 0:
        st.markdown("### 第一關：想吃什麼？")
        st.write("請聽聲音：")
        play_audio("hemay", filename_base="u6_hemay")
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🍚 hemay"):
                st.balloons()
                st.success("答對了！ Hemay 是飯！")
                time.sleep(1)
                st.session_state.score += 100
                st.session_state.current_q += 1
                st.rerun()
        with c2:
            if st.button("💧 nanom"): st.error("不對喔，nanom 是水！")

    # 第二關：句子理解 (喜好)
    elif st.session_state.current_q == 1:
        st.markdown("### 第二關：我喜歡什麼？")
        st.markdown("#### 請聽句子：")
        play_audio("Maolah kako to pawli.", filename_base="u6_s_like_banana")
        
        st.write("請問句子裡的人喜歡什麼？")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🍌 香蕉 (pawli)"):
                st.snow()
                st.success("沒錯！ Maolah kako to pawli.")
                time.sleep(1)
                st.session_state.score += 100
                st.session_state.current_q += 1
                st.rerun()
        with c2:
            if st.button("🍠 地瓜 (konga)"): st.error("不對喔！")

    # 第三關：看圖問答 (綜合練習)
    elif st.session_state.current_q == 2:
        st.markdown("### 第三關：看圖回答")
        st.markdown("#### Q: O maan koni? (這是什麼？)")
        play_audio("O maan koni?", filename_base="u6_q_what") 
        
        st.markdown("<div style='font-size:80px; text-align:center;'>🍊</div>", unsafe_allow_html=True)
        
        options = ["O mami' (是橘子)", "O dateng (是菜)", "O hemay (是飯)"]
        choice = st.radio("請選擇：", options)
        
        if st.button("確定送出"):
            if "mami'" in choice:
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
st.sidebar.title("Unit 6: O kakaenen 🍌")
mode = st.sidebar.radio("選擇模式", ["📖 學習單詞", "🎮 練習挑戰"])

if mode == "📖 學習單詞":
    show_learning_mode()
else:
    show_quiz_mode()
