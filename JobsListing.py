import os
import streamlit as st
import requests

# --- Sidebar with Instructions ---
st.sidebar.title("How to Use the App")
st.sidebar.markdown(
    """
    **Job Search App Instructions:**

    1. **Enter a Job Query:**  
       Specify the job role and location. For example, "Developer jobs in Chicago".

    2. **Select Employment Type:**  
       Choose among All, Full-time, Part-time, Contractor, or Entry Level.

    3. **Set Salary Range:**  
       Use the slider to select your desired salary range.

    4. **Remote Filter:**  
       Select if you want to search for remote, onsite, or all types of jobs.

    5. **Search:**  
       Click the **Search** button to fetch job listings based on your criteria.

    Use the collapsible sections under each job card to read the full job description.
    """
)

# --- Main App Title ---
st.title("Job Search App")

# --- User Inputs ---
job_query = st.text_input("Enter job search query (Specify Role and Location)", value="Developer jobs in Chicago")
employment_type = st.radio("Select Employment Type", options=["All", "Full-time", "Part-time", "Contractor", "Entry Level"])
salary_range = st.slider("Select Salary Range ($)", 0, 350000, (50000, 100000), step=15000)
remote_filter = st.radio("Remote Jobs Only?", options=["All", "Yes", "No"])

# Initialize session state for search results
if "jobs" not in st.session_state:
    st.session_state.jobs = None  # Stores job results

# --- Define the Modal Dialog ---
@st.dialog("Contact for Access", width="small")
def contact_modal():
    st.write("To access additional pages, please contact Josh Poresky:")
    st.write("📧 Email: [Josh.Poresky@gmail.com](mailto:Josh.Poresky@gmail.com)")
    st.markdown('[🔗 Contact me on LinkedIn](https://www.linkedin.com/in/josh-poresky956/)',
        unsafe_allow_html=True
    )    
    if st.button("Close"):
        st.session_state.show_modal = False
        st.rerun()

# --- Search Functionality ---
if st.button("Search"):
    query = job_query
    if employment_type != "All":
        query += f" {employment_type}"
    if remote_filter == "Yes":
        query += " remote"
    elif remote_filter == "No":
        query += " onsite"

    # Retrieve the RapidAPI key
    rapid_api_key = os.getenv("RapidAPI") if os.getenv("RapidAPI") else st.secrets["rapidapi"]["key"]
    url = "https://jsearch.p.rapidapi.com/search"
    querystring = {
        "query": query,
        "page": "1",
        "num_pages": "1",
        "country": "us",
        "date_posted": "all"
    }
    headers = {
        "x-rapidapi-key": rapid_api_key,
        "x-rapidapi-host": "jsearch.p.rapidapi.com"
    }

    try:
        with st.spinner("Searching for jobs..."):
            response = requests.get(url, headers=headers, params=querystring)
            response.raise_for_status()
        data = response.json()
        st.session_state.jobs = data.get("data", [])  # Store results in session state
    except requests.exceptions.RequestException:
        st.error("Something went wrong while fetching jobs. Please try again later.")
        st.session_state.jobs = None

# --- Display Jobs ---
if st.session_state.jobs:
    for job in st.session_state.jobs:
        job_title = job.get("job_title", "No Title")
        employer_name = job.get("employer_name", "N/A")
        job_location = job.get("job_location", "N/A")
        job_employment_type = job.get("job_employment_type", "N/A")
        posted_date = job.get("job_posted_at", "N/A")
        full_description = job.get("job_description", "No description available.")
        apply_link = job.get("job_apply_link", "#")

        # Enhanced job card formatting
        st.markdown(f"""
        <div style="padding: 15px; border: 1px solid #ddd; border-radius: 10px; margin-bottom: 15px; background-color: #f9f9f9;">
            <h3 style="margin-bottom: 5px;">{job_title}</h3>
            <p><strong>Employer:</strong> {employer_name}</p>
            <p><strong>Location:</strong> {job_location}</p>
            <p><strong>Employment Type:</strong> {job_employment_type}</p>
            <p><strong>Posted:</strong> {posted_date}</p>
            <a href="{apply_link}" target="_blank" style="color: #007BFF; text-decoration: none; font-weight: bold;">Apply Here</a>
        </div>
        """, unsafe_allow_html=True)

        # Collapsible Job Description.
        with st.expander("View Job Description"):
            st.write(full_description)
        st.markdown("---")

    # --- Pagination ---
    if st.button("Next Page"):
        st.session_state.show_modal = True

# --- Display Modal if Triggered ---
if st.session_state.get("show_modal", False):
    contact_modal()

# --- Footer ---
st.markdown(
    """
    <hr>
    <p style="text-align: center;">
    <b>Jobst Listing Application</b> &copy; 2025<br>
    Developed by <a href="https://www.linkedin.com/in/josh-poresky956/" target="_blank">Josh Poresky</a><br><br>
    </p>
    """,
    unsafe_allow_html=True
)
