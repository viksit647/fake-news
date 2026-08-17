import streamlit as st
import pickle

# Load model
with open("random_forest_fake_news.pkl", "rb") as f:
    model = pickle.load(f)

# Page config
st.set_page_config(
    page_title="VeriNews",
    page_icon="",
    layout="wide"
)

# Simple styling
st.markdown("""
<style>
    .main {
        max-width: 1100px;
        margin: auto;
    }

    .title {
        font-size: 52px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 18px;
        color: #666;
        margin-bottom: 35px;
    }

    .result {
        padding: 25px;
        border-radius: 16px;
        border: 1px solid #ddd;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="title">VeriNews</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">AI-powered fake news detection using machine learning.</div>',
    unsafe_allow_html=True
)

st.divider()

# Main layout
left, right = st.columns([1.4, 1])

with left:
    st.subheader("Analyze an article")

    article = st.text_area(
        "Paste news article text",
        height=350,
        placeholder="Paste the full article here..."
    )

    analyze = st.button(
        "Analyze Article",
        type="primary",
        use_container_width=True
    )

with right:
    st.subheader("Prediction")

    if analyze:
        if not article.strip():
            st.warning("Please enter some article text.")
        else:
            prediction = model.predict([article])[0]
            probabilities = model.predict_proba([article])[0]

            fake_probability = probabilities[0]
            real_probability = probabilities[1]

            if prediction == 0:
                st.error("FAKE NEWS")
            else:
                st.success("REAL NEWS")

            st.metric(
                "Confidence",
                f"{max(fake_probability, real_probability) * 100:.2f}%"
            )

            st.write(
                f"Fake probability: **{fake_probability * 100:.2f}%**"
            )

            st.progress(float(fake_probability))

            st.write(
                f"Real probability: **{real_probability * 100:.2f}%**"
            )

            st.progress(float(real_probability))

    else:
        st.info("Enter an article and click **Analyze Article**.")

st.divider()

# Model information
st.subheader("Model")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Model", "Random Forest")

with col2:
    st.metric("Features", "TF-IDF")

with col3:
    st.metric("Max Features", "5,000")

st.caption(
    "Prediction is based on the language patterns learned by the trained model. "
    "It does not independently verify whether the underlying event is true."
)
