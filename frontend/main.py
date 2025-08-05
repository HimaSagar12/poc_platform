
import streamlit as st
import requests
import pandas as pd

# API base URL
API_URL = "http://127.0.0.1:8000"

# --- Helper Functions ---
def login(email, password):
    response = requests.post(f"{API_URL}/token", data={"username": email, "password": password})
    if response.status_code == 200:
        st.session_state.token = response.json()["access_token"]
        return True
    return False

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

def post_comment(poc_id, text):
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    response = requests.post(f"{API_URL}/comments", headers=headers, json={"text": text, "poc_id": poc_id})
    return response.status_code == 200

def create_poc(title, description):
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    response = requests.post(f"{API_URL}/pocs", headers=headers, json={"title": title, "description": description})
    return response.status_code == 200

def get_my_pocs():
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    response = requests.get(f"{API_URL}/users/me/pocs", headers=headers)
    if response.status_code == 200:
        return response.json()
    return []

def get_my_applications():
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    response = requests.get(f"{API_URL}/users/me/applications", headers=headers)
    if response.status_code == 200:
        return response.json()
    return []

# --- Streamlit App ---
st.set_page_config(page_title="Recruitment Platform", layout="wide")

# --- State Management ---
if "token" not in st.session_state:
    st.session_state.token = None
if "page" not in st.session_state:
    st.session_state.page = "home"

# --- Navigation ---
st.sidebar.title("Navigation")
if st.session_state.token:
    if st.sidebar.button("Dashboard"):
        st.session_state.page = "dashboard"
    if st.sidebar.button("Logout"):
        st.session_state.token = None
        st.session_state.page = "home"
else:
    if st.sidebar.button("Home"):
        st.session_state.page = "home"
    if st.sidebar.button("Login"):
        st.session_state.page = "login"
    if st.sidebar.button("Register"):
        st.session_state.page = "register"

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

elif st.session_state.page == "login":
    st.title("Login")
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        if submitted:
            if login(email, password):
                st.session_state.page = "dashboard"
                st.experimental_rerun()
            else:
                st.error("Invalid email or password")

elif st.session_state.page == "register":
    st.title("Register")
    with st.form("register_form"):
        full_name = st.text_input("Full Name")
        email = st.text_input("Email")
        designation = st.text_input("Designation")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Register")
        if submitted:
            if register(full_name, email, designation, password):
                st.success("Registration successful! Please login.")
                st.session_state.page = "login"
                st.experimental_rerun()
            else:
                st.error("Registration failed")

elif st.session_state.page == "dashboard":
    st.title("Dashboard")
    st.header("My Posted POCs")
    my_pocs = get_my_pocs()
    if my_pocs:
        st.dataframe(pd.DataFrame(my_pocs))
    else:
        st.write("You haven't posted any POCs yet.")

    st.header("My Applications")
    my_applications = get_my_applications()
    if my_applications:
        st.dataframe(pd.DataFrame(my_applications))
    else:
        st.write("You haven't applied to any POCs yet.")

    st.header("Create New POC")
    with st.form("create_poc_form"):
        title = st.text_input("Title")
        description = st.text_area("Description")
        submitted = st.form_submit_button("Create POC")
        if submitted:
            if create_poc(title, description):
                st.success("POC created successfully!")
                st.experimental_rerun()
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

        if st.session_state.token:
            with st.form("comment_form"):
                text = st.text_area("Write a comment...")
                submitted = st.form_submit_button("Post Comment")
                if submitted:
                    if post_comment(poc_id, text):
                        st.success("Comment posted successfully!")
                        st.experimental_rerun()
                    else:
                        st.error("Failed to post comment")
