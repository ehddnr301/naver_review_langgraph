import streamlit as st

from llm_utils.graph import builder
from langchain_core.messages import HumanMessage
from streamlit.components.v1 import html


st.set_page_config(page_title="🍔 맛집 추천 서비스", layout="wide")

st.title("🍔 맛집 추천 서비스")
my_html = """
<style>
    #log {
        font-family: Arial, sans-serif;
        color: white; /* 무난한 색상 */
        display:flex;
        align-items: center;
    }
    .spinner {
        margin-right:10px;
        transform: translateY(-50%);
        border: 4px solid #f3f3f3; /* Light grey */
        border-top: 4px solid #3498db; /* Blue */
        border-radius: 50%;
        width: 20px;
        height: 20px;
        animation: spin 1s linear infinite;
    }
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
</style>
<script>
function logResponses() {
    var logContainer = document.querySelector('#log');
    setInterval(function () {
        fetch('http://34.16.215.193:9999')
            .then(response => response.text())
            .then(data => {
                if (data !== '""') {
                    logContainer.innerHTML = '<div class="spinner"></div>'; // Clear the container and add spinner
                    var logEntry = document.createElement('div');
                    logEntry.textContent = data.replaceAll('"', "");
                    logContainer.appendChild(logEntry);
                }
                else {
                    // clear
                    logContainer.innerHTML = '';
                }
            })
            .catch(error => {
                var logEntry = document.createElement('div');
                logEntry.textContent = 'Error: ' + error;
                logContainer.appendChild(logEntry);
            });
    }, 1000);  // Send request every second
}

window.onload = function () {
    logResponses();
};
</script>

<body>
  <div id="log">
  </div>
</body>
"""


if "responses" not in st.session_state:
    st.session_state.responses = []

st.write("### Responses")
response_container = st.container()

for response in st.session_state.responses:
    with response_container:
        st.text(response)
html(my_html, height=50)

col1, col2 = st.columns([4, 1])

with col1:
    input_text = st.text_input("Enter your query:", key="input_text")

with col2:
    if st.button("Submit"):
        graph = builder.compile()
        if input_text:
            st.session_state.responses = []
            human_message = HumanMessage(content=input_text)

            res = graph.invoke(input=human_message)
            response = f"""
                질문: {input_text}\n
                {res[-1].content}
            """
            response = response.replace("                ", "")
            print("-" * 100)
            print(response)
            print("-" * 100)
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
