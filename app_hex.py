"""
VeriNews — Streamlit app redesigned with a Hex.tech-inspired look.

Design choices translated from hex.tech:
- Near-black top bar (like Hex's header) with a serif-italic logo and bold tagline
- Warm off-white canvas background (#FAFAF8)
- White rounded cards with 1px borders and soft shadows
- Dark filled primary buttons + outlined secondary buttons (pill-ish, rounded)
- Monospace "eyebrow" labels above cards (Hex's card captions)
- Result shown in a floating result card with a status badge, big confidence metric,
  and probability bars
- Model info as a row of small metric cards
"""
import streamlit as st
import pickle
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- Load model
model_path = os.path.join(BASE_DIR, "random_forest_fake_news.pkl")
with open(model_path, "rb") as f:
    model = pickle.load(f)

# ---------------------------------------------------------------- Page setup
st.set_page_config(
    page_title="VeriNews — AI Fake News Detection",
    page_icon="hexagon" if hasattr(st, "page_icon") else "🔷",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------------- Theme CSS
st.markdown("""
<style>
    /* ---------- Base ---------- */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital@1&family=Inter:wght@400;500;600;700&family=IBM+Plex+Mono&display=swap');

    .reportview-container .main .block-container {
        padding-top: 0px;
        padding-left: 0px;
        padding-right: 0px;
        max-width: 100%;
    }

    /* ---------- Compact centered content wrapper ---------- */
    .hex-wrap {
        max-width: 1120px;
        width: 100%;
        margin: 0 auto;
    }

    /* ---------- Header (Hex-style dark bar) ---------- */
    .hex-header {
        background: #0F1114;
        border-bottom: 1px solid #23262E;
        padding: 16px 40px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .hex-logo {
        font-family: 'Playfair Display', serif;
        font-style: italic;
        font-size: 30px;
        font-weight: 600;
        color: #FFFFFF;
        letter-spacing: 0.5px;
    }
    .hex-logo strong {
        font-family: 'Inter', sans-serif;
        font-style: normal;
        font-weight: 700;
        color: #A78BFA;  /* violet accent */
    }
    .hex-tagline {
        font-family: 'Inter', sans-serif;
        font-size: 14px;
        color: #9CA3AF;
        font-weight: 500;
    }

    /* ---------- Hero ---------- */
    .hex-hero {
        background: linear-gradient(180deg, #F4F3F0 0%, #FAFAF8 100%);
        padding: 44px 40px 24px 40px;
        text-align: center;
    }
    .hex-eyebrow {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 12px;
        color: #7C3AED;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 14px;
    }
    .hex-title {
        font-family: 'Playfair Display', serif;
        font-style: italic;
        font-size: 42px;
        color: #111827;
        line-height: 1.15;
        margin-bottom: 4px;
    }
    .hex-title strong {
        font-family: 'Inter', sans-serif;
        font-style: normal;
        font-weight: 700;
    }
    .hex-subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 17px;
        color: #6B7280;
        max-width: 640px;
        margin: 14px auto 0 auto;
        line-height: 1.6;
    }

    /* ---------- Cards ---------- */
    .hex-card {
        background: #FFFFFF;
        border: 1px solid #E8E8E5;
        border-radius: 16px;
        box-shadow: 0 1px 2px rgba(17,24,39,0.05), 0 8px 24px rgba(17,24,39,0.06);
        padding: 28px;
        margin-bottom: 24px;
    }
    .hex-card-label {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 11px;
        color: #9CA3AF;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 6px;
    }
    .hex-card-title {
        font-family: 'Inter', sans-serif;
        font-size: 18px;
        font-weight: 600;
        color: #111827;
        margin-bottom: 14px;
    }

    /* ---------- Inputs styled like Hex cards ---------- */
    .stTextArea textarea, .stTextInput input {
        font-family: 'Inter', sans-serif !important;
        font-size: 15px !important;
        border-radius: 12px !important;
        background: #F9F9F7 !important;
        border: 1px solid #E8E8E5 !important;
    }
    .stTextArea textarea:focus, .stTextInput input:focus {
        border: 1.5px solid #7C3AED !important;
    }
    /* Card wrapper for the input area and its button */
    .input-card {
        background: #FFFFFF;
        border: 1px solid #E8E8E5;
        border-radius: 14px;
        box-shadow: 0 1px 2px rgba(17,24,39,0.05), 0 8px 24px rgba(17,24,39,0.06);
        padding: 22px 24px 24px 24px;
        margin-top: 4px;
    }
    .input-card textarea {
        background: #F9F9F7 !important;
    }

    /* ---------- Buttons ---------- */
    .stButton button {
        font-family: 'Inter', sans-serif !important;
        font-size: 15px !important;
        font-weight: 600 !important;
        border-radius: 10px !important;
        padding: 0.45rem 1.6rem !important;
        transition: all 0.15s ease;
    }
    div[data-testid="stFormSubmitButton"] button,
    .stButton button[kind="primary"] {
        background: #111827 !important;
        color: #FFFFFF !important;
        border: 1px solid #111827 !important;
    }
    div[data-testid="stFormSubmitButton"] button:hover,
    .stButton button[kind="primary"]:hover {
        background: #7C3AED !important;
        border-color: #7C3AED !important;
    }

    /* ---------- Result ---------- */
    .verdict {
        display: inline-block;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 15px;
        letter-spacing: 1px;
        padding: 6px 16px;
        border-radius: 999px;
        margin-bottom: 10px;
    }
    .verdict-fake { background: #FEE2E2; color: #B91C1C; }
    .verdict-real { background: #D1FAE5; color: #047857; }
    .conf-number {
        font-family: 'Inter', sans-serif;
        font-size: 44px;
        font-weight: 700;
        color: #111827;
        line-height: 1;
    }
    .conf-label {
        font-family: 'Inter', sans-serif;
        font-size: 13px;
        color: #6B7280;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 2px;
    }
    .prob-text {
        font-family: 'Inter', sans-serif;
        font-size: 14px;
        color: #374151;
    }
    .prob-text b { color: #111827; }

    /* ---------- Metric chips ---------- */
    .metric-chip {
        background: #F7F7F5;
        border: 1px solid #E8E8E5;
        border-radius: 12px;
        padding: 14px 18px;
        text-align: center;
    }
    .metric-chip .mc-label {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 10.5px;
        color: #9CA3AF;
        text-transform: uppercase;
        letter-spacing: 1.2px;
    }
    .metric-chip .mc-value {
        font-family: 'Inter', sans-serif;
        font-size: 16px;
        font-weight: 600;
        color: #111827;
        margin-top: 4px;
    }

    .footnote {
        font-family: 'Inter', sans-serif;
        font-size: 12.5px;
        color: #9CA3AF;
        margin-top: 6px;
        line-height: 1.6;
    }
    hr.hex-divider { border: none; border-top: 1px solid #E8E8E5; margin: 8px 0 32px 0; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------- Header
st.markdown("""
<div class="hex-header">
    <div class="hex-wrap">
        <div style="display: flex; align-items: center; justify-content: space-between;">
            <div class="hex-logo">Veri<em>News</em><span style="color: #A78BFA; font-family: 'Inter', sans-serif; font-weight: 700;">.</span></div>
            <div class="hex-tagline">AI-powered fake news detection &nbsp;·&nbsp; Random Forest + TF-IDF</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------- Hero
st.markdown("""
<div class="hex-hero">
    <div class="hex-wrap">
        <div class="hex-eyebrow">machine learning · text classification</div>
        <div class="hex-title">Know if a story is <em>trustworthy</em>,<br><strong>before you share it.</strong></div>
    <div class="hex-subtitle">
        Paste any news article below. Our model reads the language patterns and returns a
        verdict with a confidence score — in seconds.
    </div>
    </div>
</div>
<div style="height: 14px;"></div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------- Input card
st.markdown('<div class="hex-wrap">', unsafe_allow_html=True)
col_left, col_right = st.columns([1.5, 1])

with col_left:
    st.markdown(
        '<div style="display:flex; align-items:center; gap:10px; margin-bottom: 14px;">'
        '<span style="font-family: \'IBM Plex Mono\', monospace; font-size: 11px; color: #9CA3AF; text-transform: uppercase; letter-spacing: 1.5px;">// input</span>'
        '<span style="font-family: \'Inter\', sans-serif; font-size: 18px; font-weight: 600; color: #111827;">Analyze an article</span>'
        '</div>',
        unsafe_allow_html=True,
    )

    article = st.text_area(
        "Paste the full article text",
        height=280,
        placeholder="Paste the complete article text here — the more context, the more accurate the verdict…",
        label_visibility="collapsed",
    )

    analyze = st.button("Analyze article", type="primary", use_container_width=True)

    if analyze and not article.strip():
        st.warning("Please paste some article text before analyzing.")

    # The textarea container + the button sit below markdown blocks, so we
    # style them as Hex cards with pure CSS (:has() is supported in all modern
    # browsers, including Streamlit Cloud).
    st.markdown(
        "<style>"
        "div[data-testid=stColumn] > div[data-testid=stVerticalBlock]:has(div.stTextArea) {"
        "  background: #FFFFFF; border: 1px solid #E8E8E5; border-radius: 14px;"
        "  box-shadow: 0 1px 2px rgba(17,24,39,0.05), 0 8px 24px rgba(17,24,39,0.06);"
        "  padding: 6px 24px 20px 24px !important; margin-top: 4px !important;"
        "}"
        "div[data-testid=stColumn] > div[data-testid=stVerticalBlock]:has(div.stTextArea) textarea {"
        "  background: #F9F9F7 !important;"
        "}"
        "div[data-testid=stColumn] > div[data-testid=stVerticalBlock]:has(div.stButton) > div.stButton {"
        "  background: #FFFFFF; border: 1px solid #E8E8E5; border-radius: 14px;"
        "  box-shadow: 0 1px 2px rgba(17,24,39,0.05), 0 8px 24px rgba(17,24,39,0.06);"
        "  padding: 14px !important; margin-top: 12px !important;"
        "}"
        "</style>",
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------------- Result card
with col_right:
    st.markdown(
        '<div class="hex-card" style="padding-bottom: 20px;">'
        '<div style="display:flex; align-items:center; gap:10px;">'
        '<span style="font-family: \'IBM Plex Mono\', monospace; font-size: 11px; color: #9CA3AF; text-transform: uppercase; letter-spacing: 1.5px;">// output</span>'
        '<span style="font-family: \'Inter\', sans-serif; font-size: 18px; font-weight: 600; color: #111827;">Prediction</span>'
        '</div>'
        '<div style="margin-top: 16px;">',
        unsafe_allow_html=True,
    )

    if analyze and article.strip():
        prediction = model.predict([article])[0]
        probabilities = model.predict_proba([article])[0]
        fake_probability = probabilities[0]
        real_probability = probabilities[1]

        verdict_class = "verdict-fake" if prediction == 0 else "verdict-real"
        verdict_text = "FAKE NEWS" if prediction == 0 else "REAL NEWS"

        st.markdown(f"""
        <span class="verdict {verdict_class}">● {verdict_text}</span>
        <div style="margin-top: 12px;"></div>
        <div class="conf-label">Confidence</div>
        <div class="conf-number">{max(fake_probability, real_probability) * 100:.1f}%</div>
        """, unsafe_allow_html=True)

        st.markdown('<div style="height: 18px;"></div>', unsafe_allow_html=True)

        fake_color = "#EF4444" if prediction == 0 else "#D1D5DB"
        real_color = "#10B981" if prediction == 1 else "#D1D5DB"

        st.markdown(
            f"""
            <div style="height: 10px; border-radius: 5px; background: #EDEDED; overflow: hidden;">
                <div style="width: {fake_probability * 100:.1f}%; height: 100%; background: {fake_color}; border-radius: 5px;"></div>
            </div>
            <p class="prob-text">Fake probability: <b>{fake_probability * 100:.1f}%</b></p>
            <div style="height: 10px; border-radius: 5px; background: #EDEDED; overflow: hidden; margin-top: 12px;">
                <div style="width: {real_probability * 100:.1f}%; height: 100%; background: {real_color}; border-radius: 5px;"></div>
            </div>
            <p class="prob-text">Real probability: <b>{real_probability * 100:.1f}%</b></p>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown("""
        <div style="background: #F7F7F5; border: 1px dashed #E4E4E0; border-radius: 12px;
                    padding: 26px 20px; text-align: center;">
            <div style="font-family: 'IBM Plex Mono', monospace; font-size: 11px;
                        color: #9CA3AF; text-transform: uppercase; letter-spacing: 1.5px;
                        margin-bottom: 8px;">waiting for input</div>
            <p style="font-family: 'Inter', sans-serif; font-size: 14px; color: #6B7280;
                      margin: 0;">Paste an article and press <b>Analyze article</b>
            to see the verdict here.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div></div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------------- Model info
st.markdown("""
<div class="hex-wrap">
    <div style="padding: 0 4px; margin-top: 26px;">
        <div class="hex-card-label" style="padding-left: 6px;">// about this model</div>
        <div class="hex-card-title" style="padding-left: 6px; margin-bottom: 18px;">How it works</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="hex-wrap">', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("""
    <div class="metric-chip">
        <div class="mc-label">Algorithm</div>
        <div class="mc-value">Random Forest</div>
    </div>""", unsafe_allow_html=True)
with c2:
    st.markdown("""
    <div class="metric-chip">
        <div class="mc-label">Features</div>
        <div class="mc-value">TF-IDF</div>
    </div>""", unsafe_allow_html=True)
with c3:
    st.markdown("""
    <div class="metric-chip">
        <div class="mc-label">Vocabulary</div>
        <div class="mc-value">5,000 terms</div>
    </div>""", unsafe_allow_html=True)

st.markdown("""
<p class="footnote">
    Predictions are based on language patterns learned from a labeled corpus of real and
    fake news articles. The model does not independently verify whether the underlying
    event is true. Short inputs (headlines only) may produce less reliable results.
</p>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
