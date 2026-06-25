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
    }
    
    /* Wrap everything inside a clean custom container class */
    .main-card {
        background-color: rgba(0,0,0,0.75);
        padding: 30px;
        border-radius: 12px;
        color: white;
    }

    .result-box {
        background-color: rgba(20, 20, 20, 0.9);
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

# --- Main Container UI ---
# Using a native Streamlit container with an HTML class wrapper avoids unclosed div errors
with st.container():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    
    # --- Title ---
    st.title("🔧 VVI AI Assistant")
    st.caption("Velan Valves Intelligence – Ask anything or analyze files")
    
    # --- Show response on TOP ---
    if st.session_state.response:
        st.markdown(f"""
        <div class="result-box">
            <h4 style="color: #4CAF50; margin-top:0;">✅ Response:</h4>
            <p style="white-space: pre-wrap;">{st.session_state.response}</p>
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
                    # ✅ Case 1: Processing with an uploaded file
                    if uploaded_file is not None:
                        mime_type, _ = mimetypes.guess_type(uploaded_file.name)
                        mime_type = mime_type or "application/octet-stream"
                        
                        # Read bytes directly from the Streamlit object
                        file_bytes = uploaded_file.read()
                        
                        # Pass data inline using the correct SDK structure
                        response = client.models.generate_content(
                            model="gemini-2.5-flash", # Adjusted to standard flash model
                            contents=[
                                {
                                    "mime_type": mime_type,
                                    "data": file_bytes
                                },
                                question
                            ]
                        )

                    # ✅ Case 2: Text prompt only
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
