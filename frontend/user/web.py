import json

import streamlit as st
import requests

from settings import Settings


def user():
    chat_container = st.container(height=300, key='user')
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
                st.session_state['chat_history']):  # Отображаем в обратном порядке, чтобы новые сообщения были наверху
            st.markdown(
                f'<div class="chat-message"><b>{msg["sender"]}</b>: {msg["serial_number_check_result"]}<br>{msg["completeness_check_result"]} <br> {msg["equipment_name_check_result"]}</div>',
                unsafe_allow_html=True)

    st.subheader("Пользователь")
    path = Settings()
    path = path.backend_base_url
    # Форма для ввода темы и тела сообщения
    with st.form(key='user_form'):
        user_subject = str(st.text_input("Тема"))
        user_body = str(st.text_area("Тело"))
        submit_button = st.form_submit_button(label="Отправить")

        if submit_button:
            url = f'{path}/message'

            data = {'title': user_subject, 'body': user_body}
            headers = {"Content-Type": "application/json"}
            response = requests.post(url, headers=headers, data=json.dumps(data)).json()

            if response['type'] == 'to_agent':
                st.session_state['chat_history_operator'].append(
                    {"sender": 'Пользователь', "subject": user_subject, "body": user_body,
                     "serial_number": response['serial_number_check_result']['data'],
                     "type_of_equipment": response['classification_result']['equipment_type'],
                     "point_of_failure": response['classification_result']['point_of_failure']})
                st.rerun()
            else:
                st.session_state['chat_history'].append(
                    {
                        "sender": 'Bot',
                        "serial_number_check_result": response['serial_number_check_result']['text'],
                        "completeness_check_result": response['completeness_check_result']['text'],
                        "equipment_name_check_result": response['equipment_name_check_result']['text']
                    }
                )
                st.rerun()
