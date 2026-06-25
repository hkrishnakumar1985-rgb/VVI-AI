import streamlit as st
from google import genai
import mimetypes

# --- Page Setup ---
st.set_page_config(page_title="VVI AI Assistant", layout="centered")

# --- Gemini Client ---
client = genai.Client(api_key=st.secrets["MY_API_KEY"])

# --- Background Image + Styling ---
st.markdown("""
    <style>
    .stApp {
        background-image: url('https://images.unsplash.com/photo-1565449434612-7d3a7c4a13ba');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: white;
    }

    .overlay {
        background-color: rgba(0,0,0,0.75);
        padding: 20px;
        border-radius: 12px;
    }

    .result-box {
        background-color: rgba(0,0,0,0.8);
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
    }

    .stTextInput input {
        background-color: #1e293b;
        color: white;
    }

    .stButton button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        height: 45px;
        width: 100%;
        font-size: 16px;
    }
    </style>
""", unsafe_allow_html=True)

# --- Main Container ---
st.markdown('<div class="overlay">', unsafe_allow_html=True)

# --- Title ---
st.title("🔧 VVI AI Assistant")
st.caption("Velan Valves Intelligence – Ask anything or analyze files")

# --- Session state ---
if "response" not in st.session_state:
    st.session_state.response = ""

# ✅ Show response on TOP
if st.session_state.response:
    st.markdown(f"""
    <div class="result-box">
        <h4>✅ Response:</h4>
        <p>{st.session_state.response}</p>
    </div>
    """, unsafe_allow_html=True)

# --- File Upload ---
uploaded_file = st.file_uploader("📂 Upload file (PDF / Excel / TXT)")

# --- Question ---
question = st.text_input("💬 Ask your question:")

# --- Button ---
if st.button("🚀 Get Answer"):

    if not question:
        st.warning("Please enter a question")

    else:
        with st.spinner("Processing..."):
            try:
                # ✅ With file
                if uploaded_file is not None:

                    mime_type, _ = mimetypes.guess_type(uploaded_file.name)

                    file_data = client.files.upload(
                        file=uploaded_file,
                        config={"mime_type": mime_type or "application/octet-stream"}
                    )

                    response = client.models.generate_content(
                        model="gemini-flash-lite-latest",
                        contents=[question, file_data]
                    )

                # ✅ Without file
                else:
                    response = client.models.generate_content(
                        model="gemini-flash-lite-latest",
                        contents=question
                    )

                st.session_state.response = response.text
                st.rerun()

            except Exception as e:
                st.error(f"❌ Error: {e}")

st.markdown('</div>', unsafe_allow_html=True)
