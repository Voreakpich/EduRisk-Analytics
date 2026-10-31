
# Step 1: Import required libraries
import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu

# Step 2: Page Configuration ---
st.set_page_config(
    page_title="EduRisk Analytics - Lab 03",
    page_icon="🎓",
    layout="wide"
) 
# Add a CSV Loading Function
def load_student_data():
    try:
        data = pd.read_csv("students.csv")
        return data
    except FileNotFoundError:
        st.error(
            "students.csv was not found. Please place it in the same folder as app.py."
        )
        st.stop()
# Load the Student Data
student_df = load_student_data() 

# Step 3 (Style): Blue background and global styling
# Injecting custom CSS to completely redesign the Streamlit app's look and feel
st.markdown("""
<style>
    /* Cream/Beige gradient background for the main content area */
    /* linear-gradient creates a smooth transition between two light colors */
    [data-testid='stAppViewContainer'] {
        background: linear-gradient(135deg, #FFFDD0, #F5F5DC);
    }

    /* Light background for the top header bar where the menu button is */
    [data-testid='stHeader'] {
        background: #FFFDD0 !important;
    }

    /* Make all header/toolbar button icons dark so they are visible on the light background */
    header button svg, header button span {
        fill: #333333 !important;
        color: #333333 !important;
    }

    /* Force the sidebar collapse/expand button (top left arrow) to have a transparent background */
    [data-testid='stSidebarCollapsedControl'] {
        background: transparent !important;
    }
    
    /* Style the sidebar collapse button to have a subtle border and rounded corners */
    [data-testid='stSidebarCollapsedControl'] button {
        background: transparent !important;
        border: 1px solid rgba(0,0,0,0.2) !important;
        border-radius: 6px !important;
    }
    
    /* Ensure the icon inside the sidebar collapse button remains dark */
    [data-testid='stSidebarCollapsedControl'] button svg,
    [data-testid='stSidebarCollapsedControl'] button span,
    [data-testid='stSidebarNavItems'] button svg,
    section[data-testid='stSidebar'] button svg {
        fill: #333333 !important;
        color: #333333 !important;
    }

    /* Premium Sidebar Background & Design */
    /* This targets the actual left sidebar container */
    [data-testid='stSidebar'] {
        background: #F0EAD6 !important; /* Soft warm beige */
        border-right: 1px solid rgba(0, 0, 0, 0.05) !important; /* Very faint line separating it from main app */
    }

    /* Global font configuration: Sets the font family, default text color, and base size */
    html, body, p, div, label, li, a {
        font-family: 'Times New Roman', Times, serif !important;
        color: #333333 !important; /* Dark grey instead of pure black for softer contrast */
        font-size: 18px !important;
    }

    /* Fix dropdown list text color (make it dark on white background) */
    /* This ensures Streamlit selectboxes remain readable when clicked */
    div[data-baseweb="popover"] div, 
    div[data-baseweb="popover"] span,
    ul[role="listbox"] li, 
    ul[role="listbox"] span {
        color: #0a1628 !important;
    }

    /* Metric cards premium styling (Light Theme) */
    /* Adds a "Glassmorphism" effect to the metrics (Students, Average Score, etc.) */
    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.6); /* Semi-transparent white */
        border: 1px solid rgba(0, 0, 0, 0.1); /* Subtle dark border */
        border-radius: 12px; /* Rounded corners */
        padding: 15px; /* Inner spacing */
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05); /* Soft drop shadow below the card */
        backdrop-filter: blur(10px); /* Blurs the background behind the card */
    }
    [data-testid="stMetricLabel"] {
        color: #555555 !important;
        font-size: 14px !important;
    }
    [data-testid="stMetricValue"] {
        color: #333333 !important;
        font-size: 32px !important;
        font-weight: bold;
    }

    /* Heading sizes */
    h1 { font-size: 38px !important; }
    h2 { font-size: 28px !important; }
    h3 { font-size: 26px !important; }
</style>
""", unsafe_allow_html=True)

# Step 3: Sample Student Data ---

# Step 4: Add a risk levels function ---
def get_risk_level(score, attendance):
    if score < 60 or attendance < 60:
        return "High Risk"
    elif score < 75 or attendance < 75:
        return "Medium Risk"
    else:
        return "Low Risk"

# Add a risk levels column ---
student_df["Risk Level"] = student_df.apply(
    lambda row: get_risk_level(
        row["Score"],
        row["Attendance"]
    ),
    axis=1
)

# Step 5b: Risk level color map for charts
risk_color_map = {
    "Low Risk": "#9CBF96",     # Soft Sage Green
    "Medium Risk": "#E4C580",  # Soft Mustard/Gold
    "High Risk": "#D98A7F"     # Soft Terracotta/Rose
}

# Step 5c: Function to highlight risk levels in dataframes
def highlight_risk(val):
    if val == "High Risk":
        return "background-color: #D98A7F; color: #333333; font-weight: bold;"
    elif val == "Medium Risk":
        return "background-color: #E4C580; color: #333333; font-weight: bold;"
    elif val == "Low Risk":
        return "background-color: #9CBF96; color: #333333; font-weight: bold;"
    return ""

# Step 6: Compute Summary Statistics ---
total_students = len(student_df)
average_score = student_df["Score"].mean()
average_attendance = student_df["Attendance"].mean()
low_score_students = student_df[student_df["Score"] < 60].shape[0]

# Initialize session state variables before page routing
if "risk_history" not in st.session_state:
    st.session_state["risk_history"] = []

# Step 7: Sidebar Navigation ---
# Using streamlit_option_menu for a premium, icon-based navigation menu
with st.sidebar:
    selected_page = option_menu(
        menu_title="EduRisk", # Title at the top of the menu card
        options=["Home", "Dashboard", "Student Data", "Risk Checker", "About"], # The actual tabs/pages
        icons=["house", "speedometer2", "table", "shield-check", "info-circle"], # Bootstrap icons for each tab
        menu_icon="mortarboard", # The icon next to the "EduRisk" title
        default_index=0, # Home is selected by default
        styles={
            # Container is the floating card wrapping the whole menu
            "container": {"padding": "15px", "background-color": "rgba(255, 255, 255, 0.5)", "border-radius": "10px", "border": "1px solid rgba(0,0,0,0.1)"},
            # Style for the icons next to each page name
            "icon": {"color": "#333333", "font-size": "18px"}, 
            # Style for each unselected page link
            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "margin-bottom": "5px", "--hover-color": "rgba(255,255,255,0.8)", "color": "#333333"},
            # Style for the currently active/selected page
            "nav-link-selected": {"background-color": "white", "color": "#333333", "font-weight": "bold", "box-shadow": "0 2px 5px rgba(0,0,0,0.05)"},
            # Style for the "EduRisk" title at the top
            "menu-title": {"color": "#333333", "font-weight": "bold", "font-size": "22px", "padding-bottom": "15px"}
        }
    )

# Step 8: Home Page ---
if selected_page == "Home":
    st.title("🎓 EduRisk Analytics")
    st.subheader("Frontend Prototype with CSV Data Loading")
    st.write("Welcome to Lab 03.")
    st.write(
        "In this lab, the app loads student data from students.csv "
        "using Pandas instead of storing data directly inside app.py."
    )
    st.success("Lab 03 app is running successfully!")

# -- Step 24: Update the Student Data Page
elif selected_page == "Student Data":
    st.title("Student Data")

    st.write(
        "This page displays and inspects the dataset loaded from students.csv."
    )

    st.subheader("Data Inspection")

    # Show shape as two metric cards
    shape_col1, shape_col2 = st.columns(2)
    with shape_col1:
        st.metric("Total Rows", student_df.shape[0])
    with shape_col2:
        st.metric("Total Columns", student_df.shape[1])

    # Show column names as styled badges
    st.write("Column Names:")
    badge_html = " ".join([
        f'<span style="background-color:#E4C580; color:#333333; padding:4px 10px; '
        f'border-radius:12px; font-size:13px; font-weight:bold; margin:3px; '
        f'display:inline-block;">{col}</span>'
        for col in student_df.columns.tolist()
    ])
    st.markdown(badge_html, unsafe_allow_html=True)

    st.write("")

    st.write("First 5 Rows:")
    styled_head = student_df.head().style.map(highlight_risk, subset=["Risk Level"])
    st.dataframe(styled_head, use_container_width=True)

    st.subheader("Full Student Dataset")
    styled_df = student_df.style.map(highlight_risk, subset=["Risk Level"])
    st.dataframe(styled_df, use_container_width=True)

# -- Step 25: Create the Risk Checker Page
elif selected_page == "Risk Checker":
    st.title("Single Student Risk Checker")

    st.write(
        "Enter student information to check risk level. "
        "The result is based on score and attendance."
    )

    st.info(
        "This tool is for academic support. Risk results should help students, "
        "not label or punish them."
    )

    with st.form("risk_checker_form"):
        input_name = st.text_input("Student Name")
        input_score = st.number_input("Score", 0, 100, 50)
        input_attendance = st.number_input("Attendance", 0, 100, 50)

        submitted = st.form_submit_button("Check Risk")

    if submitted:
        if input_name.strip() == "":
            st.warning("Please enter the student name.")
        else:
            result = {
                "Student Name": input_name.strip(),
                "Score": input_score,
                "Attendance": input_attendance,
                "Risk Level": get_risk_level(input_score, input_attendance)
            }
            st.session_state["risk_history"].append(result)
            if result["Risk Level"] == "Low Risk":
                st.success("Risk Level: Low Risk")
                st.write("Student appears on track.")
            elif result["Risk Level"] == "Medium Risk":
                st.warning("Risk Level: Medium Risk")
                st.write("Monitor progress and provide guidance.")
            else:
                st.error("Risk Level: High Risk")
                st.write("Student may need additional support.")
# Show the submitted student information after checking risk                
            st.write("Student Name:", input_name.strip())
            st.write("Score:", input_score)
            st.write("Attendance:", input_attendance)   

# Add recent risk checks section
    st.subheader("Recent Risk Checks")
    if len(st.session_state["risk_history"]) > 0:
        history_df = pd.DataFrame(
            st.session_state["risk_history"]
        )

        st.dataframe(history_df)
        if st.button("Clear History"):
            st.session_state["risk_history"] = []
            st.success("Risk check history cleared.")
    else:
        st.info("No risk checks yet.")       

# Add ethics reminder to risk checker
    st.warning(
        "Ethics Reminder: Risk results should be used as guidance for support, "
        "not as final judgment about a student."
    )
# Step 9: Design Dashboard Code
elif selected_page == "Dashboard":
    st.title("Dashboard Prototype")

    st.write(
        "This dashboard gives a quick overview of student performance "
        "using data loaded from students.csv."
    )

    total_students = len(student_df)
    average_score = student_df["Score"].mean()
    average_attendance = student_df["Attendance"].mean()
    high_risk_students = student_df[
        student_df["Risk Level"] == "High Risk"
    ].shape[0]

    st.subheader("Dashboard Metrics")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Students", total_students)

    with col2:
        st.metric("Average Score", round(average_score, 2))

    with col3:
        st.metric("Average Attendance", f"{round(average_attendance, 2)}%")

    with col4:
        st.metric("High Risk", high_risk_students)

    st.subheader("Student Records")
    st.write("This table shows student data loaded from students.csv.")
    styled_table = student_df.style.map(highlight_risk, subset=["Risk Level"])
    st.dataframe(styled_table, use_container_width=True)

    st.subheader("Charts")

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.write("Student Score Chart")
        fig_score = px.bar(
            student_df,
            x="Student Name",
            y="Score",
            color="Risk Level",
            color_discrete_map=risk_color_map,
            text="Score"
        )
        fig_score.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#333333", family="Times New Roman", size=14),
            xaxis=dict(gridcolor="rgba(0,0,0,0.1)"),
            yaxis=dict(gridcolor="rgba(0,0,0,0.1)"),
            showlegend=True,
            margin=dict(t=30, b=40, l=40, r=20)
        )
        fig_score.update_traces(textposition="outside")
        st.plotly_chart(fig_score, use_container_width=True)

    with chart_col2:
        st.write("Course Count")
        course_count = student_df["Course"].value_counts().reset_index()
        course_count.columns = ["Course", "Count"]
        fig_course = px.pie(
            course_count,
            names="Course",
            values="Count",
            color_discrete_sequence=["#9CBF96", "#E4C580", "#D98A7F", "#7FB3D3", "#C3A8D1"],
            hole=0.4
        )
        fig_course.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#333333", family="Times New Roman", size=14),
            showlegend=True,
            margin=dict(t=30, b=20, l=20, r=20)
        )
        fig_course.update_traces(textinfo="label+percent", textposition="outside")
        st.plotly_chart(fig_course, use_container_width=True)

    st.info(
        "Ethics Reminder: Academic monitoring should support students, "
        "not label or punish them."
    ) 

# -- Step 20: Add Show or Hide Dataset Checkbox
    show_data = st.checkbox("Show Filtered Dataset", True)

    if show_data:
        st.subheader("Student Dataset")
        styled_filtered = student_df.style.map(highlight_risk, subset=["Risk Level"])
        st.dataframe(styled_filtered)
    else: 

# -- Step 21: Add Download Button
        st.info("Dataset is hidden.") 
        csv = student_df.to_csv(index=False)

        st.download_button(
            label="Download Filtered Data",
            data=csv,
            file_name="filtered_student_data.csv",
            mime="text/csv"
        ) 
# -- Step 22: Add Student Score Chart
    st.subheader("Charts")

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.write("Student Scores")

        if len(student_df) > 0:
            # Create a Plotly bar chart
            fig_score = px.bar(
                student_df,
                x="Student Name",
                y="Score",
                color="Risk Level",
                color_discrete_map=risk_color_map, # Apply the pastel colors we defined in Step 5b
                text="Score" # Show the actual score number above the bar
            )
            # Update the chart layout to blend with our cream background
            fig_score.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", # Makes the outer background transparent
                plot_bgcolor="rgba(0,0,0,0)",  # Makes the inner plot background transparent
                font=dict(color="#333333", family="Times New Roman", size=14), # Dark text for readability
                xaxis=dict(gridcolor="rgba(0,0,0,0.1)"), # Subtle dark gridlines
                yaxis=dict(gridcolor="rgba(0,0,0,0.1)"),
                showlegend=False, # Hide the legend since colors are self-explanatory
                margin=dict(t=30, b=40, l=40, r=20) # Trim margins so it fits nicely
            )
            fig_score.update_traces(textposition="outside") # Put the text label outside the top of the bar
            st.plotly_chart(fig_score, use_container_width=True) # Render chart in Streamlit
        else:
            st.warning("No data available for score chart.") 

# -- Step 23: Add Risk Level Count Chart
    with chart_col2:
        st.write("Risk Level Count")

        if len(student_df) > 0:
            # First, count how many students fall into each risk level
            risk_count = student_df["Risk Level"].value_counts().reset_index()
            risk_count.columns = ["Risk Level", "Count"]
            
            # Create the bar chart for the counts
            fig_risk = px.bar(
                risk_count,
                x="Risk Level",
                y="Count",
                color="Risk Level",
                color_discrete_map=risk_color_map,
                text="Count"
            )
            # Apply the exact same layout modifications as the first chart
            fig_risk.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#333333", family="Times New Roman", size=14),
                xaxis=dict(gridcolor="rgba(0,0,0,0.1)"),
                yaxis=dict(gridcolor="rgba(0,0,0,0.1)"),
                showlegend=False,
                margin=dict(t=30, b=40, l=40, r=20)
            )
            fig_risk.update_traces(textposition="outside")
            st.plotly_chart(fig_risk, use_container_width=True)
        else:
            st.warning("No data available for risk chart.")


# Step 26: About Page ---
else:
    st.title("About")

    st.write("This app is part of Lab 04.")
    st.write("Course: Web App Development for Data Science")
    st.write("Project Theme: EduRisk Analytics")
    st.write("Topic: Forms, Validation, and Session State")

    st.info(
        "This version improves the Risk Checker page using Streamlit forms, "
        "input validation, and session state."
    )

    st.warning(
        "Ethics Reminder: Student risk information should be used responsibly "
        "to support learning and student success."
    )