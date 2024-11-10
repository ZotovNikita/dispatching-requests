import streamlit as st
from operaor.web import operator
from user.web import user


def main():
    st.set_page_config(page_title="Диспечеризация заявок", layout="wide")

    st.markdown(
        """
        <style>
        [data-testid="stSidebar"][aria-expanded="true"] > div:first-child{
            width: 400px;
        }
        [data-testid="stSidebar"][aria-expanded="false"] > div:first-child{
            width: 400px;
            margin-left: -400px;
        }
        

        h3 {text-align: center;}
        h1 {
        padding-top: 0%;
        }
        .st-emotion-cache-12fmjuu {
            background: #f27979;
        }
        .stLogo{
        width:100%;
        height: 5rem;
        }
        header{
        color:white;
        }
        """,
        unsafe_allow_html=True,
    )
    st.logo('static/logo.svg',size="large")
    st.title("Почта 📪")
    st.markdown(
        """
        <style>
        .block-container {
            padding-left: 5rem;  /* Вы можете изменить значение для увеличения/уменьшения расстояния */
            padding-right: 1rem;  /* Вы можете изменить значение для увеличения/уменьшения расстояния */
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

    if 'chat_history_operator' not in st.session_state:
        st.session_state['chat_history_operator'] = []

    col1, col2 = st.columns(2, gap="large")
    with col1:
        # Область для отображения сообщений
        st.subheader("Письма от модели ✉")
        user()
    with col2:
        operator()


if __name__ == "__main__":
    main()
