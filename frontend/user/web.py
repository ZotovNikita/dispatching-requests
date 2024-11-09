import json

import streamlit as st
import requests


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
            st.markdown(f'<div class="chat-message"><b>{msg["sender"]}</b>: {msg["subject"]}<br>{msg["body"]}</div>',
                        unsafe_allow_html=True)

    st.subheader("Пользователь")

    # Форма для ввода темы и тела сообщения
    with st.form(key='user_form'):
        user_subject = str(st.text_input("Тема"))
        user_body = str(st.text_area("Тело"))
        submit_button = st.form_submit_button(label="Отправить")

        if submit_button:
            url = 'http://dr_backend:8558/message'

            data = {'title': user_subject, 'body': user_body}
            headers = {"Content-Type": "application/json"}
            response = requests.post(url, headers=headers, data=json.dumps(data)).json()

            st.session_state['chat_history_operator'].append(
                {"sender": 'Пользователь', "subject": user_subject, "body": user_body,
                 "serial_number": response['serial_number'],
                 "type_of_equipment": response['type_of_equipment']})

            st.session_state['chat_history'].append(
                {"sender": 'Пользователь', "subject": user_subject, "body": user_body})
