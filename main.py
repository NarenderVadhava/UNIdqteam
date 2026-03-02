import streamlit as st
import importlib
import os

st.set_page_config(page_title="Python Validation`", layout="wide")
st.title("DV")

project_files = [
    f for f in os.listdir("project")
    if f.endswith(".py") and f != "__init__.py"
]

project_names = [i.replace(".py", "") for i in project_files]

selected_project = st.selectbox("Select Project", project_names)

if selected_project:
    module = importlib.import_module(f"project.{selected_project}")
    module.run()