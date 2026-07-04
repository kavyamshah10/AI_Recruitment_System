"""
helpers.py
--------------------------------------
Common helper functions used
throughout the project.
"""

import streamlit as st


# ==========================================
# Load CSS
# ==========================================

def load_css(file_name):
    """
    Load external CSS file.
    """

    try:

        with open(file_name) as css:

            st.markdown(
                f"<style>{css.read()}</style>",
                unsafe_allow_html=True
            )

    except FileNotFoundError:

        st.warning(
            "CSS file not found."
        )


# ==========================================
# Page Title
# ==========================================

def page_title(title):
    """
    Display page title.
    """

    st.markdown(
        f"""
        <h1 style='
        text-align:center;
        color:#2563EB;'>
        {title}
        </h1>
        """,
        unsafe_allow_html=True
    )


# ==========================================
# Success Message
# ==========================================

def success(message):

    st.success(message)


# ==========================================
# Error Message
# ==========================================

def error(message):

    st.error(message)


# ==========================================
# Resume Score
# ==========================================

def show_resume_score(score):
    """
    Display score using
    progress bar.
    """

    st.subheader("Resume Score")

    st.progress(score)

    st.write(f"### {score}/100")


# ==========================================
# Status Badge
# ==========================================

def show_status(status):

    if status == "Selected":

        st.success("✅ Selected")

    elif status == "Rejected":

        st.error("❌ Rejected")

    else:

        st.warning(status)


# ==========================================
# Section Divider
# ==========================================

def divider():

    st.markdown("---")