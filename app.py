import streamlit as st

from llm_utils.graph import graph
from langchain_core.messages import HumanMessage

st.set_page_config(page_title="🍔 맛집 추천 서비스", layout="wide")

st.title("🍔 맛집 추천 서비스")

if "responses" not in st.session_state:
    st.session_state.responses = []

st.write("### Responses")
response_container = st.container()

for response in st.session_state.responses:
    with response_container:
        st.text(response)
        st.write("---")  # 구분선 추가

col1, col2 = st.columns([4, 1])

with col1:
    input_text = st.text_input("Enter your query:", key="input_text")

with col2:
    if st.button("Submit"):
        if input_text:
            human_message = HumanMessage(content=input_text)

            res = graph.invoke(input=human_message)
            response = f"""
                질문: {input_text}\n
                {res[-1].content}
            """
            response = response.replace("                ", "")

            st.session_state.responses.append(response)
            st.rerun()

st.markdown(
    """
        <style>
        .stTextInput, .stButton {
            margin-bottom: 0 !important;
        }
        .stButton {
            margin-top: 30px;
        }
        </style>
    """,
    unsafe_allow_html=True,
)
