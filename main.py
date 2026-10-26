import streamlit as st
from input_module import render_blog_inputs
from blog_module import generate_blog
from title_module import generate_titles
from summary_module import generate_summary
from keyword_module import generate_keywords
from meta_module import generate_meta_description
from intent_module import detect_intent
from utils import ollama_status, save_blog, MODEL

st.set_page_config(page_title="AI Blog Generator", page_icon="✍️", layout="wide")
st.title("AI Blog Content Generator")
st.caption(f"Powered by Ollama · {MODEL}")

with st.sidebar:
    st.subheader("Model connection")
    st.write(f"Model: `{MODEL}`")
    if st.button("Check Ollama connection"):
        ok, message = ollama_status()
        (st.success if ok else st.error)(message)
    st.markdown("Start Ollama locally and pull the model before using the app:")
    st.code("ollama pull qwen3:4b\nollama serve", language="bash")
    st.divider()
    st.caption("Ollama API: http://localhost:11434")

tab_blog, tab_tools, tab_chat = st.tabs(
    ["Generate a blog", "SEO tools", "Ask by intent"]
)

with tab_blog:
    topic, style, tone, word_count = render_blog_inputs()
    if st.button("Generate complete blog", type="primary", use_container_width=True):
        if not topic.strip():
            st.warning("Enter a blog topic first.")
        else:
            with st.spinner("Qwen is writing your blog..."):
                try:
                    blog = generate_blog(topic, style, tone, word_count)
                    st.session_state["blog"] = blog
                    st.session_state["topic"] = topic
                    st.success("Blog generated.")
                except Exception as e:
                    st.error(str(e))
    if st.session_state.get("blog"):
        blog = st.session_state["blog"]
        st.subheader("Generated blog")
        st.markdown(blog)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Save blog to outputs/generated_blog.txt"):
                path = save_blog(blog)
                st.success(f"Saved to {path}")
        with col2:
            st.download_button("Download blog as TXT", blog, file_name="generated_blog.txt",
                               mime="text/plain", use_container_width=True)

with tab_tools:
    blog = st.text_area("Blog text", value=st.session_state.get("blog", ""),
                        height=240, placeholder="Paste a blog or generate one in the first tab.")
    topic = st.session_state.get("topic", "")
    selected = st.selectbox("Choose a tool", [
        "Generate 5 titles", "Generate SEO keywords",
        "Generate a 100-word summary", "Generate meta description"
    ])
    if st.button("Run SEO tool", type="primary"):
        if not blog.strip() and not topic.strip():
            st.warning("Generate a blog or enter blog text first.")
        else:
            source = blog.strip() or f"Topic: {topic}"
            with st.spinner("Generating..."):
                try:
                    if selected == "Generate 5 titles":
                        result = generate_titles(source)
                    elif selected == "Generate SEO keywords":
                        result = generate_keywords(source)
                    elif selected == "Generate a 100-word summary":
                        result = generate_summary(source)
                    else:
                        result = generate_meta_description(source)
                    st.session_state["seo_result"] = result
                    st.session_state["seo_tool"] = selected
                except Exception as e:
                    st.error(str(e))
    if st.session_state.get("seo_result"):
        st.subheader(st.session_state.get("seo_tool", "Result"))
        st.write(st.session_state["seo_result"])
        st.download_button("Download result", st.session_state["seo_result"],
                           file_name="seo_result.txt", mime="text/plain")

with tab_chat:
    st.write("Describe what you need in natural language. The intent detector routes the request.")
    request = st.text_input("Your request", placeholder="Example: Give SEO keywords for a blog about AI in education")
    if st.button("Detect intent and run", type="primary"):
        if not request.strip():
            st.warning("Enter a request.")
        else:
            with st.spinner("Detecting intent..."):
                try:
                    intent = detect_intent(request)
                    st.info(f"Detected intent: **{intent}**")
                    source = st.session_state.get("blog", "") or request
                    if intent == "BLOG_GENERATION":
                        result = generate_blog(request, "Professional", "Informative", 500)
                        st.session_state["blog"] = result
                        st.session_state["topic"] = request
                    elif intent == "SUMMARY":
                        result = generate_summary(source)
                    elif intent == "KEYWORD_GENERATION":
                        result = generate_keywords(source)
                    elif intent == "META_DESCRIPTION":
                        result = generate_meta_description(source)
                    elif intent == "TITLE_GENERATION":
                        result = generate_titles(source)
                    else:
                        result = "I couldn't identify the task. Try asking for a blog, title, summary, keywords, or meta description."
                    st.markdown(result)
                    st.session_state["intent_result"] = result
                except Exception as e:
                    st.error(str(e))
