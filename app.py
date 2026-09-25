import streamlit as st
import os
from dotenv import load_dotenv

from spreadsheet_parser import load_excel, create_dataframe_context
from agent import ask_claude

# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------

load_dotenv()

st.set_page_config(
    page_title="Services Project ROI Agent",
    page_icon="📊",
    layout="wide"
)

# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "spreadsheet_context" not in st.session_state:
    st.session_state.spreadsheet_context = None

if "file_name" not in st.session_state:
    st.session_state.file_name = None


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.title("📊 Services Project ROI Agent")

st.write(
    "Upload your Services Project ROI spreadsheet and "
    "ask questions or make assumptions about the model."
)

# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

with st.sidebar:

    st.header("📁 Spreadsheet")

    uploaded_file = st.file_uploader(
        "Upload Excel file",
        type=["xlsx", "xls"],
        help="Upload your Services Project ROI Excel file."
    )

    if uploaded_file:

        if st.session_state.file_name != uploaded_file.name:

            with st.spinner("Reading spreadsheet..."):

                try:

                    spreadsheet_context = (
                        create_dataframe_context(
                            uploaded_file
                        )
                    )

                    st.session_state.spreadsheet_context = (
                        spreadsheet_context
                    )

                    st.session_state.file_name = (
                        uploaded_file.name
                    )

                    st.session_state.messages = []

                    st.success(
                        "Spreadsheet loaded successfully!"
                    )

                except Exception as e:

                    st.error(
                        f"Error reading spreadsheet: {e}"
                    )
    # -----------------------------------------------------
    # Spreadsheet information
    # -----------------------------------------------------

    if st.session_state.spreadsheet_context:

        st.divider()

        st.subheader("📋 Sheets")

        for sheet_name in (
            st.session_state.spreadsheet_context.keys()
        ):

            df = (
                st.session_state.spreadsheet_context[
                    sheet_name
                ]
            )

            st.write(
                f"**{sheet_name}**  \n"
                f"{df.shape[0]} rows × "
                f"{df.shape[1]} columns"
            )

        st.divider()

        # Clear conversation
        if st.button(
            "🗑️ Clear Conversation",
            use_container_width=True
        ):

            st.session_state.messages = []

            st.rerun()


# ---------------------------------------------------------
# CHECK SPREADSHEET
# ---------------------------------------------------------

if not st.session_state.spreadsheet_context:

    st.info(
        "👈 Upload your Excel spreadsheet from the sidebar "
        "to start chatting with the ROI Agent."
    )

    st.stop()


# ---------------------------------------------------------
# DISPLAY PREVIOUS MESSAGES
# ---------------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(
            message["content"]
        )


# ---------------------------------------------------------
# CHAT INPUT
# ---------------------------------------------------------

user_prompt = st.chat_input(
    "Ask about the spreadsheet or make an assumption..."
)


# ---------------------------------------------------------
# PROCESS USER MESSAGE
# ---------------------------------------------------------

if user_prompt:

    # Display user message
    with st.chat_message("user"):

        st.markdown(user_prompt)

    # Store user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_prompt
        }
    )

    # -----------------------------------------------------
    # Ask Claude
    # -----------------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner(
            "Analyzing spreadsheet..."
        ):

            try:

                # Convert spreadsheet data into text
                spreadsheet_context = ""

                for (
                    sheet_name,
                    df
                ) in st.session_state.spreadsheet_context.items():

                    spreadsheet_context += (
                        f"\n\n"
                        f"===== SHEET: {sheet_name} =====\n\n"
                    )

                    spreadsheet_context += (
                        df.to_string(index=False)
                    )

                # Send to Claude
                response = ask_claude(
                    user_prompt,
                    spreadsheet_context
                )

                st.markdown(response)

                # Save assistant response
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": response
                    }
                )

            except Exception as e:

                error_message = (
                    f"❌ Error: {str(e)}"
                )

                st.error(error_message)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": error_message
                    }
                )