import streamlit as st
import requests
import os 
from dotenv import load_dotenv
load_dotenv()
API_URL = os.getenv("API_URL")

st.set_page_config(page_title="Research Future Scope Finder", layout="wide")
st.title(" Future Scope Research Assistant")

user_query = st.text_input("Enter a research topic (e.g., 'Lithium Battery', 'AI in Healthcare')")

if st.button("Get Future Scope"):
    if not user_query.strip():
        st.warning("Please enter a valid research topic.")
    else:
        with st.spinner("Analyzing... Please wait"):
            try:
                response = requests.post(
                    API_URL,
                    json={"research_on": user_query.strip()}
                )
                if response.status_code == 200:
                    result = response.json()
                    if result["status"] == "success":
                        st.success(result["message"])
                        st.markdown("### Research Report")
                        st.markdown(result["data"])
                    else:
                        st.error(result["message"])
                        if "error" in result:
                            st.code(result["error"])
                else:
                    st.error(f"API call failed with status {response.status_code}")
                    st.code(response.text)
            except Exception as e:
                st.error("Failed to connect to the backend.")
                st.code(str(e))
