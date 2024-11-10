import streamlit as st

def operator():
    st.subheader('Оператор 👩🏻‍💻')
    chat_container = st.container(height=670, key='operator')
    with chat_container:
        st.markdown("""
                    <style>
                    .chat-box {
                        max-height: 300px;
                        overflow-y: auto;
                    }
                    </style>
                    <div class="chat-box">
                    """, unsafe_allow_html=True)

        for msg in reversed(
                st.session_state['chat_history_operator']):  # Отображаем в обратном порядке, чтобы новые сообщения были наверху
            st.markdown(f'<div class="chat-message"><b>{msg["sender"]}</b>: <br><b>Заголовок:</b> {msg["subject"]}<br> <b>Тело письма: </b>{msg["body"]} <br> '
                        f'<b>Серийный номер: </b> {msg["serial_number"]} <br> '
                        f'<b>Тип аппаратуры: </b>{msg["type_of_equipment"]}</div>'
                        f'<b>Точка отказа: </b>{msg["point_of_failure"]} <br> <br>',
                        unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

