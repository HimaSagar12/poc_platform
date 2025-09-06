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

def get_applications_for_poc(poc_id):
    response = requests.get(f"{API_URL}/applications/poc/{poc_id}")
    if response.status_code == 200:
        return response.json()
    return []

def get_my_pocs(owner_id):
    response = requests.get(f"{API_URL}/pocs/owner/{owner_id}")
    if response.status_code == 200:
        return response.json()
    return []

def delete_poc(poc_id, owner_id):
    response = requests.delete(f"{API_URL}/pocs/{poc_id}?owner_id={owner_id}")
    return response.status_code == 200

def get_applications_by_applicant(applicant_id):
    response = requests.get(f"{API_URL}/applications/applicant/{applicant_id}")
    if response.status_code == 200:
        return response.json()
    return []

def update_application_status(application_id, status):
    response = requests.put(f"{API_URL}/applications/{application_id}/status?status={status}")
    return response.status_code == 200

# --- Streamlit App ---
st.set_page_config(page_title="Recruitment Platform", layout="wide")

# --- State Management ---
if "page" not in st.session_state:
    st.session_state.page = "home"

# Global user selection
users = get_users()
user_names = {user["full_name"]: user["id"] for user in users}
if "current_user_id" not in st.session_state:
    st.session_state.current_user_id = None
    st.session_state.current_user_name = "Select User"

st.sidebar.title("Select User")
selected_user_name_sidebar = st.sidebar.selectbox(
    "Choose your account:",
    ["Select User"] + list(user_names.keys()),
    index=0,
    key="global_user_select"
)

if selected_user_name_sidebar != "Select User":
    st.session_state.current_user_id = user_names[selected_user_name_sidebar]
    st.session_state.current_user_name = selected_user_name_sidebar
else:
    st.session_state.current_user_id = None
    st.session_state.current_user_name = "Select User"

st.sidebar.write(f"Current User: **{st.session_state.current_user_name}**")

# --- Navigation ---
st.sidebar.title("Navigation")
if st.sidebar.button("Home"):
    st.session_state.page = "home"
if st.sidebar.button("Register User"):
    st.session_state.page = "register_user"
if st.sidebar.button("Create POC"):
    st.session_state.page = "create_poc"
if st.sidebar.button("View Applications"):
    st.session_state.page = "view_applications"
if st.sidebar.button("My POCs"):
    st.session_state.page = "my_pocs"
if st.sidebar.button("My Applications"):
    st.session_state.page = "my_applications"

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
    if st.session_state.current_user_id:
        owner_id = st.session_state.current_user_id
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
    else:
        st.warning("Please select a user from the sidebar to create a POC.")

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

        if st.session_state.current_user_id:
            author_id = st.session_state.current_user_id
            with st.form("comment_form"):
                text = st.text_area("Write a comment...")
                submitted = st.form_submit_button("Post Comment")
                if submitted:
                    if post_comment(poc_id, text, author_id):
                        st.success("Comment posted successfully!")
                        st.rerun()
                    else:
                        st.error("Failed to post comment")
        else:
            st.warning("Please select a user from the sidebar to post a comment.")

        st.header("Apply for this POC")
        if st.session_state.current_user_id:
            applicant_id = st.session_state.current_user_id
            if st.button("Apply for this POC"):
                if create_application(poc_id, applicant_id):
                    st.success("Application submitted successfully!")
                    st.rerun()
                else:
                    st.error("Failed to submit application.")
        else:
            st.warning("Please select a user from the sidebar to apply for this POC.")

        # Application Management for POC Owner
        st.header("Manage Applications")
        if st.session_state.current_user_id:
            manager_id = st.session_state.current_user_id
            if poc['owner']['id'] == manager_id:
                applications_for_poc = get_applications_for_poc(poc_id)
                if applications_for_poc:
                    for app in applications_for_poc:
                        st.write(f"**Applicant:** {app['applicant']['full_name']} ({app['applicant']['designation']})")
                        current_status = app['status']
                        new_status = st.selectbox(
                            "Update Status",
                            ["Submitted", "Under Review", "Accepted", "Rejected", "Selected"],
                            index=["Submitted", "Under Review", "Accepted", "Rejected", "Selected"].index(current_status),
                            key=f"status_{app['id']}"
                        )
                        if new_status != current_status:
                            if update_application_status(app['id'], new_status):
                                st.success(f"Application status for {app['applicant']['full_name']} updated to {new_status}!")
                                st.rerun()
                            else:
                                st.error("Failed to update application status.")
                        st.write("---")
                else:
                    st.write("No applications for this POC yet.")
            else:
                st.info("You are not the owner of this POC, so you cannot manage applications.")
        else:
            st.warning("Please select a user from the sidebar to manage applications.")

elif st.session_state.page == "view_applications":
    st.title("View Applications")
    pocs = get_pocs()
    poc_options = {poc["title"]: poc["id"] for poc in pocs}
    selected_poc_title = st.selectbox("Select POC", list(poc_options.keys()))
    poc_id = poc_options[selected_poc_title]

    applications = get_applications_for_poc(poc_id)
    if applications:
        for app in applications:
            st.write(f"**Applicant:** {app['applicant']['full_name']} ({app['applicant']['designation']})")
            st.write(f"**Status:** {app['status']}")
            st.write("---")
    else:
        st.write("No applications found for this POC.")

elif st.session_state.page == "my_pocs":
    st.title("My POCs")
    if st.session_state.current_user_id:
        owner_id = st.session_state.current_user_id
        my_pocs = get_my_pocs(owner_id)
        if my_pocs:
            for poc in my_pocs:
                with st.container():
                    st.subheader(poc["title"])
                    st.write(poc["description"])
                    if st.button("Delete", key=f"delete_poc_{poc['id']}"):
                        if delete_poc(poc["id"], owner_id):
                            st.success("POC deleted successfully!")
                            st.rerun()
                        else:
                            st.error("Failed to delete POC.")
                    if st.button("View Details", key=f"my_poc_details_{poc['id']}"):
                        st.session_state.page = "poc_details"
                        st.session_state.poc_id = poc["id"]
        else:
            st.write("You have not posted any POCs yet.")
    else:
        st.warning("Please select a user from the sidebar to view your POCs.")

elif st.session_state.page == "my_applications":
    st.title("My Applications")
    if st.session_state.current_user_id:
        applicant_id = st.session_state.current_user_id
        my_applications = get_applications_by_applicant(applicant_id)
        if my_applications:
            for app in my_applications:
                with st.container():
                    st.subheader(f"POC: {app['poc']['title']}")
                    st.write(f"Status: {app['status']}")
                    st.write(f"Description: {app['poc']['description']}")
                    st.write("---")
        else:
            st.write("You have not applied to any POCs yet.")
    else:
        st.warning("Please select a user from the sidebar to view your applications.")
