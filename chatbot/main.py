import streamlit as st
import os
import time
from models import Message
from utils import *
from db import MySQLConnection

ROLE_USER = "user"
ROLE_ASSISTANT = "assistant"
MESSAGES = "messages"

mysql_host = os.getenv("MYSQL_HOST")
mysql_port = os.getenv("MYSQL_PORT")
mysql_user = os.getenv("MYSQL_USER")
mysql_password = os.getenv("MYSQL_PASSWORD")
mysql_database = os.getenv("MYSQL_DATABASE")

connection = MySQLConnection(host=mysql_host, port=mysql_port, user=mysql_user, password=mysql_password,
                             database=mysql_database)
connection.connect()
questions = load_questions()


def display_message(message):
    _role = message.role
    _content = message.content
    _content_type = message.content_type
    with st.chat_message(name=message.role):
        if _content_type == "sql":
            st.code(_content, language=_content_type, line_numbers=False)
        elif _content_type == "dataframe":
            st.dataframe(_content, hide_index=True)
        else:
            st.write(_content)


## no need to check if is a query if it is hello then error
##


# if prompt:
#     if prompt in questions:
#         _prompt_message = Message(role="user", content=prompt, content_type="text")
#         response = questions[prompt]
#         _response_message = Message(role="assistant", content=prompt, content_type="sql")
#     else:
#         result, status = connection.execute_query(prompt)
#         if "Error" in status:
#             _prompt_message = Message(role="user", content=prompt, content_type="text")
#             response = "I don't understand!"
#             _response_message = Message(role="assistant", content=response, content_type="sql")
#         else:
#             _prompt_message = Message(role="user", content=prompt, content_type="sql")
#             response = result
#             _response_message = Message(role="assistant", content=response, content_type="sql")
#
#     with st.chat_message(name="user"):
#         st.write(prompt)
#
#     with st.chat_message(name="assistant"):
#         st.write(response)
#
#     st.session_state.messages.append(_prompt_message)
#     st.session_state.messages.append(_response_message)


# def chat(prompt):
#     if prompt:
#         # check if prompt is in the pre-defined questions
#         if prompt in questions:
#             _message = Message(role="user", content=prompt, content_type="text")
#             # display_message(_message)
#             with st.chat_message(name="user"):
#                 st.write(prompt)
#             st.session_state.messages.append(_message)
#
#             # get the response sql
#             response = questions[prompt]
#             response_message = Message(role="assistant", content=response, content_type="sql")
#             with st.chat_message(name="assistant"):
#                 with st.spinner("Thinking..."):
#                     time.sleep(1)
#                 st.code(response, language="sql")
#             st.session_state.messages.append(response_message)
#         else:
#             is_valid, query_type = validate_query(prompt)
#             if is_valid:
#                 _message = Message(role="user", content=prompt, content_type="sql")
#                 # display_message(_message)
#                 with st.chat_message(name="user"):
#                     st.code(prompt, language="sql")
#
#                 st.session_state.messages.append(_message)
#                 result = connection.execute_query(prompt)
#                 response = result
#
#                 response_message = Message(role="assistant", content=response)
#                 with st.chat_message(name="assistant"):
#                     with st.spinner("Thinking..."):
#                         time.sleep(1)
#                         # st.write(response)
#                     st.dataframe(response, hide_index=True)
#                         # st.write_stream(_streaming_response_generator())
#                     st.balloons()
#                 st.session_state.messages.append(response_message)
#             else:
#                 _message = Message(role="user", content=prompt, content_type="text")
#                 st.session_state.messages.append(_message)
#                 display_message(_message)
#
#                 response = "I don't understand!"
#                 response_message = Message(role="assistant", content=response)
#
#                 with st.chat_message(name="assistant"):
#                     st.write(response)
#                     st.snow()
#                 st.session_state.messages.append(response_message)


def main():
    st.set_page_config(page_title="Data for Kids SQL Chatbot", layout="wide")
    # Add a chatbot title
    st.title("💬 Chatbot")
    st.caption("🚀 Data for Kids SQL Chatbot")

    if MESSAGES not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        display_message(message)

    # Create a prompt chat input
    prompt = st.chat_input("Please type in your message: ...")

    # Sidebar with a button to delete chat history
    with st.sidebar:
        for question in questions:
            btn = st.button(question)
            if btn:
                prompt = question

    if prompt:
        if prompt in questions:
            _prompt_message = Message(role="user", content=prompt, content_type="text")
            response = questions[prompt]
            _response_message = Message(role="assistant", content=response, content_type="sql")

            with st.chat_message(name="user"):
                st.write(prompt)
            with st.chat_message(name="assistant"):
                with st.spinner("Thinking..."):
                    time.sleep(1)
                    st.code(response, language="sql", line_numbers=False)
        else:
            result, status = connection.execute_query(prompt)
            if "Error" in status:
                _prompt_message = Message(role="user", content=prompt, content_type="text")
                response = "I don't understand!"
                _response_message = Message(role="assistant", content=response, content_type="text")
                with st.chat_message(name="user"):
                    st.write(prompt)
                # time.sleep(1)
                with st.chat_message(name="assistant"):
                    with st.spinner("Thinking..."):
                        time.sleep(1)
                        st.write(response)
                        st.snow()
            else:
                _prompt_message = Message(role="user", content=prompt, content_type="sql")
                response = result
                _response_message = Message(role="assistant", content=response, content_type="dataframe")
                with st.chat_message(name="user"):
                    st.code(prompt, language="sql", line_numbers=False)
                # time.sleep(1)
                with st.chat_message(name="assistant"):
                    with st.spinner("Thinking..."):
                        time.sleep(1)
                        st.dataframe(response, hide_index=True)
                        st.balloons()

        # with st.chat_message(name="user"):
        #     st.write(prompt)

        # with st.chat_message(name="assistant"):
        #     st.write(response)
        # display_message(_prompt_message)
        # display_message(_response_message)
        st.session_state.messages.append(_prompt_message)
        st.session_state.messages.append(_response_message)
    # chat(prompt)


if __name__ == "__main__":
    main()
