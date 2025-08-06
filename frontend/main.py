import streamlit as st
import requests
import pandas as pd

# API base URL
API_URL = "http://127.0.0.1:8000"

# --- Helper Functions ---
def register(full_name, email, designation, password):
    response = requests.post(f"{API_URL}/users", json={"full_name": full_name, "email": email, "designation": designation, "password": password})
    return response.status_code == 200

def get_pocs():
    response = requests.get(f"{API_URL}/pocs")
    if response.status_code == 200:
        return response.json()
    return []

def get_poc_details(poc_id):
    response = requests.get(f"{API_URL}/pocs/{poc_id}")
    if response.status_code == 200:
        return response.json()
    return None

def get_comments(poc_id):
    response = requests.get(f"{API_URL}/comments/poc/{poc_id}")
    if response.status_code == 200:
        return response.json()
    return []

def post_comment(poc_id, text, author_id):
    response = requests.post(f"{API_URL}/comments", json={"text": text, "poc_id": poc_id, "author_id": author_id})
    return response.status_code == 200

def create_poc(title, description, owner_id):
    response = requests.post(f"{API_URL}/pocs", json={"title": title, "description": description, "owner_id": owner_id})
    return response.status_code == 200

def create_application(poc_id, applicant_id):
    response = requests.post(f"{API_URL}/applications", json={"poc_id": poc_id, "applicant_id": applicant_id})
    return response.status_code == 200

def get_users():
    response = requests.get(f"{API_URL}/users")
    if response.status_code == 200:
        return response.json()
    return []

# --- Streamlit App ---
st.set_page_config(page_title="Recruitment Platform", layout="wide")

# --- State Management ---
if "page" not in st.session_state:
    st.session_state.page = "home"

# --- Navigation ---
st.sidebar.title("Navigation")
if st.sidebar.button("Home"):
    st.session_state.page = "home"
if st.sidebar.button("Register User"):
    st.session_state.page = "register_user"
if st.sidebar.button("Create POC"):
    st.session_state.page = "create_poc"

# --- Page Content ---
if st.session_state.page == "home":
    st.title("Available POCs")
    pocs = get_pocs()
    if pocs:
        for poc in pocs:
            with st.container():
                st.subheader(poc["title"])
                st.write(poc["description"])
                if st.button("View Details", key=f"poc_{poc['id']}"):
                    st.session_state.page = "poc_details"
                    st.session_state.poc_id = poc["id"]

elif st.session_state.page == "register_user":
    st.title("Register New User")
    with st.form("register_form"):
        full_name = st.text_input("Full Name")
        email = st.text_input("Email")
        designation = st.text_input("Designation")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Register")
        if submitted:
            if register(full_name, email, designation, password):
                st.success("Registration successful!")
                st.rerun()
            else:
                st.error("Registration failed")

elif st.session_state.page == "create_poc":
    st.title("Create New POC")
    users = get_users()
    user_options = {user["full_name"]: user["id"] for user in users}
    selected_user_name = st.selectbox("Select Owner", list(user_options.keys()))
    owner_id = user_options[selected_user_name]

    with st.form("create_poc_form"):
        title = st.text_input("Title")
        description = st.text_area("Description")
        submitted = st.form_submit_button("Create POC")
        if submitted:
            if create_poc(title, description, owner_id):
                st.success("POC created successfully!")
                st.rerun()
            else:
                st.error("Failed to create POC")

elif st.session_state.page == "poc_details":
    poc_id = st.session_state.poc_id
    poc = get_poc_details(poc_id)
    if poc:
        st.title(poc["title"])
        st.write(poc["description"])
        st.write(f"Posted by: {poc['owner']['full_name']} ({poc['owner']['designation']})")

        st.header("Comments")
        comments = get_comments(poc_id)
        if comments:
            for comment in comments:
                st.write(f"**{comment['author']['full_name']}**: {comment['text']}")

        users = get_users()
        user_options = {user["full_name"]: user["id"] for user in users}
        selected_author_name = st.selectbox("Comment as", list(user_options.keys()), key="comment_author")
        author_id = user_options[selected_author_name]

        with st.form("comment_form"):
            text = st.text_area("Write a comment...")
            submitted = st.form_submit_button("Post Comment")
            if submitted:
                if post_comment(poc_id, text, author_id):
                    st.success("Comment posted successfully!")
                    st.rerun()
                else:
                    st.error("Failed to post comment")

        st.header("Apply for this POC")
        selected_applicant_name = st.selectbox("Apply as", list(user_options.keys()), key="apply_applicant")
        applicant_id = user_options[selected_applicant_name]

        if st.button("Apply for this POC"):
            if create_application(poc_id, applicant_id):
                st.success("Application submitted successfully!")
                st.rerun()
            else:
                st.error("Failed to submit application.")
