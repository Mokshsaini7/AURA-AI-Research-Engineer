import requests
import streamlit as st

st.set_page_config(page_title="AURA Research Engine", page_icon="🔎", layout="wide")
st.title("AURA")
st.caption("AI Understanding, Retrieval & Analysis · local research retrieval baseline")
api_url = st.sidebar.text_input("API base URL", "http://127.0.0.1:8000").rstrip("/")
uploaded = st.sidebar.file_uploader("Upload PDF, TXT, or Markdown", type=["pdf", "txt", "md"])
if uploaded and st.sidebar.button("Ingest document", type="primary"):
    try:
        response = requests.post(
            f"{api_url}/ingest",
            files={"file": (uploaded.name, uploaded.getvalue(),
                            uploaded.type or "application/octet-stream")},
            timeout=120,
        )
        response.raise_for_status()
        st.sidebar.success(f"Indexed {response.json()['chunks_added']} chunks.")
    except requests.RequestException as exc:
        st.sidebar.error(f"API request failed: {exc}")

query = st.text_input("Search your research documents",
                      placeholder="What does the document say about ...?")
top_k = st.number_input("Results", min_value=1, max_value=20, value=5)
if st.button("Search evidence", type="primary", disabled=not query.strip()):
    try:
        response = requests.get(f"{api_url}/search",
                                params={"q": query, "top_k": int(top_k)}, timeout=30)
        response.raise_for_status()
        payload = response.json()
        st.subheader(f"{payload['count']} results")
        for rank, result in enumerate(payload["results"], start=1):
            with st.container(border=True):
                st.markdown(f"**{rank}. {result['source']}** · score `{result['score']:.4f}`")
                st.caption(result["chunk_id"])
                st.write(result["text"])
        if not payload["results"]:
            st.info("No matching evidence. Upload a document or try different keywords.")
    except requests.RequestException as exc:
        st.error(f"API request failed: {exc}")

try:
    stats = requests.get(f"{api_url}/stats", timeout=3).json()
    st.sidebar.metric("Indexed chunks", stats["indexed_chunks"])
    st.sidebar.metric("Documents", stats["documents"])
except requests.RequestException:
    st.sidebar.warning("Start the API to enable search and ingestion.")
