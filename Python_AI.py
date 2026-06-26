import streamlit as st
from google import genai
from google.genai.types import Part
import mimetypes
import pandas as pd
import io

# --- Page Setup ---
st.set_page_config(page_title="VVI AI Assistant", layout="centered")

# --- Gemini Client ---
client = genai.Client(api_key=st.secrets["MY_API_KEY"])

# --- Styling ---
st.markdown("""
    <style>
    .stApp {
        background-image: url('https://images.unsplash.com/photo-1565449434612-7d3a7c4a13ba');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    .main-card {
        background-color: rgba(0,0,0,0.75);
        padding: 30px;
        border-radius: 12px;
        color: white;
    }

    .result-box {
        background-color: rgba(20,20,20,0.9);
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        border: 1px solid #4CAF50;
        color: white;
    }

    .stTextInput input {
        background-color: #1e293b !important;
        color: white !important;
    }

    .stButton button {
        background-color: #4CAF50 !important;
        color: white !important;
        border-radius: 8px;
        height: 45px;
        width: 100%;
        font-size: 16px;
    }
    </style>
""", unsafe_allow_html=True)

# --- Session state ---
if "response" not in st.session_state:
    st.session_state.response = ""

# --- UI ---
with st.container():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)

    st.title("🔧 VVI AI Assistant")
    st.caption("Velan Valves Intelligence – Ask anything or analyze files")

    # Show response
    if st.session_state.response:
        st.markdown(f"""
        <div class="result-box">
            <h4 style="color:#4CAF50;">✅ Response</h4>
            <p style="white-space: pre-wrap;">{st.session_state.response}</p>
        </div>
        """, unsafe_allow_html=True)

    # Inputs
    uploaded_file = st.file_uploader("📂 Upload file (PDF / Excel / TXT)")
    question = st.text_input("💬 Ask your question:")

    if st.button("🚀 Get Answer"):
        if not question:
            st.warning("Please enter a question")
        else:
            with st.spinner("Processing..."):
                try:

                    # ✅ CASE 1: WITH FILE
                    if uploaded_file is not None:
                        file_bytes = uploaded_file.getvalue()

                        # ✅ Handle Excel separately (convert to CSV)
                        if uploaded_file.name.endswith(".xlsx"):
                            df = pd.read_excel(io.BytesIO(file_bytes), engine="openpyxl")

                            csv_buffer = io.StringIO()
                            df.to_csv(csv_buffer, index=False)

                            file_bytes = csv_buffer.getvalue().encode()
                            mime_type = "text/csv"

                        else:
                            mime_type, _ = mimetypes.guess_type(uploaded_file.name)
                            mime_type = mime_type or "application/octet-stream"

                        response = client.models.generate_content(
                            model="gemini-2.5-flash",
                            contents=[
                                question,
                                Part.from_bytes(
                                    data=file_bytes,
                                    mime_type=mime_type
                                )
                            ]
                        )

                    # ✅ CASE 2: TEXT ONLY
                    else:
                        response = client.models.generate_content(
                            model="gemini-2.5-flash",
                            contents=question
                        )

                    st.session_state.response = response.text
                    st.rerun()

                except Exception as e:
                    st.error(f"❌ Error: {e}")

    st.markdown('</div>', unsafe_allow_html=True)
