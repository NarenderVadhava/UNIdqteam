import streamlit as st

text_content = "This is a text file."

bytes_data = text_content.encode("utf-8")

st.print("Running start")
st.download_button(
    label="Download (bytes)",
    data=bytes_data,
    file_name="data.txt",
    mime="text/plain"
)
st.print("Running done.")
