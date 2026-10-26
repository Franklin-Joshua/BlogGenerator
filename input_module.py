import streamlit as st

def render_blog_inputs():
    with st.form("blog_inputs"):
        topic = st.text_input("Blog topic", placeholder="Artificial Intelligence in Education")
        col1, col2, col3 = st.columns(3)
        with col1:
            style = st.selectbox("Writing style", [
                "Professional", "Conversational", "Academic", "Persuasive",
                "Storytelling", "Technical", "Listicle"
            ])
        with col2:
            tone = st.selectbox("Tone", [
                "Formal", "Informative", "Friendly", "Persuasive",
                "Humorous", "Inspirational", "Neutral"
            ])
        with col3:
            word_count = st.number_input("Approximate word count", min_value=100,
                                         max_value=3000, value=500, step=100)
        st.form_submit_button("Apply inputs")
    st.markdown("**Your inputs**")
    st.write({
        "Blog topic": topic or "Not entered",
        "Writing style": style,
        "Tone": tone,
        "Approximate words": int(word_count)
    })
    return topic, style, tone, int(word_count)
