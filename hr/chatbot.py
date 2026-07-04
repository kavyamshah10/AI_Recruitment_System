"""
chatbot.py
-----------------------------------------
HR AI Chatbot Page
"""

import streamlit as st

from chatbot.hr_chatbot import get_chatbot_response


def chatbot_page():

    st.subheader("🤖 AI Recruitment Chatbot")

    st.info(
        """
        Ask questions about candidates.

        Examples:

        • Show Python candidates

        • Show Java candidates

        • Candidates with SQL

        • Candidates having score above 80

        • Selected candidates

        • Rejected candidates

        • Candidates with Django

        """
    )

    # -----------------------------
    # Chat History
    # -----------------------------

    if "chat_history" not in st.session_state:

        st.session_state.chat_history = []

    # -----------------------------
    # User Input
    # -----------------------------

    question = st.text_input(
        "Ask HR Chatbot"
    )

    if st.button("Search"):

        if question.strip() == "":

            st.warning("Please enter a query.")

        else:

            response = get_chatbot_response(question)

            st.session_state.chat_history.append(

                ("You", question)

            )

            st.session_state.chat_history.append(

                ("Bot", response)

            )

    # -----------------------------
    # Display Chat
    # -----------------------------

    st.markdown("---")

    for sender, message in st.session_state.chat_history:

        if sender == "You":

            st.chat_message("user").write(message)

        else:

            st.chat_message("assistant").write(message)