# streamlit_app.py

import streamlit as st
import hashlib
from blockchain import Blockchain
from datetime import datetime

# Initialize blockchain
if 'blockchain' not in st.session_state:
    st.session_state.blockchain = Blockchain()

blockchain = st.session_state.blockchain

# Title
st.title("📜 Decentralized Idea/Patent Registry")

# Tabs
tab1, tab2, tab3 = st.tabs(["🔏 Submit Idea", "🔎 Verify Idea", "📚 View Blockchain"])

# ----- Tab 1: Submit Idea -----
with tab1:
    st.header("Submit New Idea")
    name = st.text_input("Your Name")
    email = st.text_input("Your Email")
    idea_file = st.file_uploader("Upload your idea (PDF or text)", type=["pdf", "txt"])

    if st.button("Submit Idea"):
        if name and email and idea_file:
            file_content = idea_file.read()
            file_hash = hashlib.sha256(file_content).hexdigest()

            if blockchain.is_file_registered(file_hash):
                st.warning("⚠️ This idea already exists in the registry!")
            else:
                data = {
                    "name": name,
                    "email": email,
                    "filename": idea_file.name
                }
                block = blockchain.create_block(data, file_hash)
                st.success("✅ Idea submitted and stored on blockchain!")
                st.json(block)
        else:
            st.error("Please fill in all fields and upload a file.")

# ----- Tab 2: Verify Idea -----
with tab2:
    st.header("Verify an Idea")
    verify_file = st.file_uploader("Upload a file to check if it’s already registered", key="verify")

    if st.button("Check Idea"):
        if verify_file:
            content = verify_file.read()
            file_hash = hashlib.sha256(content).hexdigest()

            if blockchain.is_file_registered(file_hash):
                st.success("✅ This idea is already registered.")
            else:
                st.info("❌ This idea is not registered.")
        else:
            st.warning("Please upload a file to verify.")

# ----- Tab 3: View Chain -----
with tab3:
    st.header("View Blockchain")
    for block in blockchain.get_chain():
        st.subheader(f"Block {block['index']}")
        st.write("⏱️", datetime.fromtimestamp(block['timestamp']).strftime("%Y-%m-%d %H:%M:%S"))
        st.json(block)
