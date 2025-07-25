
import streamlit as st
import pandas as pd
from datetime import datetime
from PIL import Image
import os

st.set_page_config(page_title="S2M Coder Portal", layout="wide")
logo = Image.open("s2m-logo.png")

# Load login data
login_df = pd.read_csv("login coder 1.csv")

form_headers = [
    "Date", "Emp ID", "Emp Name", "Project", "Project Category", "Login ID", "Login Name",
    "Team Lead", "Chart ID", "Page No", "No of DOS", "No of Codes", "Error Type",
    "Error Comments", "No of Errors", "Chart Status", "Auditor Emp ID", "Auditor Emp Name"
]

def login_page():
    st.image(logo, width=150)
    st.markdown("<h2 style='color:skyblue;'>S2M Coder Login</h2>", unsafe_allow_html=True)
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in login_df["username"].values:
            user_row = login_df[login_df["Username"] == username].iloc[0]
            if password == str(user_row["Password"]):
                st.session_state.logged_in = True
                st.session_state.emp_id = user_row["Emp ID"]
                st.session_state.emp_name = user_row["Emp Name"]
                st.session_state.team_lead = user_row["Team Lead"]
                st.session_state.login_time = datetime.now()
                st.success("Login successful")
                st.experimental_rerun()
            else:
                st.error("Incorrect password")
        else:
            st.error("Username not found")

def form_page():
    st.image(logo, width=150)
    st.markdown("<h2 style='color:skyblue;'>Form Entry</h2>", unsafe_allow_html=True)
    with st.form("entry_form"):
        today = datetime.now().strftime("%Y-%m-%d")
        emp_id = st.session_state.emp_id
        emp_name = st.session_state.emp_name
        team_lead = st.session_state.team_lead
        st.write("Emp ID:", emp_id)
        st.write("Emp Name:", emp_name)
        st.write("Team Lead Name:", team_lead)

        project = st.selectbox("Project", ["Elevance MA", "Elevance ACA", "Health OS"], key="project")
        category = st.selectbox("Project Category", ["Entry", "Recheck", "QA"], key="category")
        login_names = login_df["Login Name"].unique().tolist()
        login_name = st.selectbox("Login Name", login_names, key="login_name")
        login_id = login_df[login_df["Login Name"] == st.session_state.login_name]["Login ID"].values[0]

        chart_id = st.text_input("Chart ID", key="chart_id")
        page_no = st.text_input("Page No", key="page_no")
        dos = st.text_input("No of DOS", key="dos")
        codes = st.text_input("No of Codes", key="codes")
        error_type = st.text_input("Error Type", key="error_type")
        error_comments = st.text_input("Error Comments", key="error_comments")
        no_of_errors = st.text_input("No of Errors", key="no_of_errors")
        chart_status = st.text_input("Chart Status", key="chart_status")
        auditor_emp_id = st.text_input("Auditor Emp ID", key="auditor_emp_id")
        auditor_emp_name = st.text_input("Auditor Emp Name", key="auditor_emp_name")

        submit = st.form_submit_button("Submit")
        if submit:
            new_data = pd.DataFrame([
                [today, emp_id, emp_name, st.session_state.project, st.session_state.category,
                 login_id, st.session_state.login_name, team_lead, st.session_state.chart_id, st.session_state.page_no,
                 st.session_state.dos, st.session_state.codes, st.session_state.error_type, st.session_state.error_comments,
                 st.session_state.no_of_errors, st.session_state.chart_status, st.session_state.auditor_emp_id, st.session_state.auditor_emp_name]
            ], columns=form_headers)
            new_data.to_csv("data.csv", mode="a", header=not os.path.exists("data.csv"), index=False)
            st.success("Data submitted successfully!")
            for key in [
                "project", "category", "login_name", "chart_id", "page_no", "dos", "codes",
                "error_type", "error_comments", "no_of_errors", "chart_status",
                "auditor_emp_id", "auditor_emp_name"]:
                st.session_state[key] = ""

def dashboard_page():
    st.image(logo, width=150)
    st.markdown("<h2 style='color:skyblue;'>Dashboard</h2>", unsafe_allow_html=True)
    if os.path.exists("data.csv"):
        df = pd.read_csv("data.csv")
        st.write("Total Records:", len(df))
        st.download_button("Download as Excel", data=df.to_csv(index=False), file_name="submitted_data.csv")

    login_time = st.session_state.get("login_time")
    if login_time:
        logout_time = datetime.now()
        duration = logout_time - login_time
        st.success(f"Login Duration: {str(duration).split('.')[0]}")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login_page()
else:
    page = st.sidebar.selectbox("Select Page", ["Form", "Dashboard"])
    if page == "Form":
        form_page()
    else:
        dashboard_page()
