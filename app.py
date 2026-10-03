
# Step 1: Import required libraries
import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu

# Step 2: Page Configuration ---
st.set_page_config(
    page_title="EduRisk Analytics - Lab 02",
    page_icon="🎓",
    layout="centered"
)

# Step 3 (Style): Blue background and global styling
st.markdown("""
<style>
    /* Cream/Beige gradient background for the main content area */
    [data-testid='stAppViewContainer'] {
        background: linear-gradient(135deg, #FFFDD0, #F5F5DC);
    }

    /* Light background for the top header bar */
    [data-testid='stHeader'] {
        background: #FFFDD0 !important;
    }

    /* Make all header/toolbar button icons dark */
    header button svg, header button span {
        fill: #333333 !important;
        color: #333333 !important;
    }

    /* Force sidebar collapse/expand button to dark */
    [data-testid='stSidebarCollapsedControl'] {
        background: transparent !important;
    }
    [data-testid='stSidebarCollapsedControl'] button {
        background: transparent !important;
        border: 1px solid rgba(0,0,0,0.2) !important;
        border-radius: 6px !important;
    }
    [data-testid='stSidebarCollapsedControl'] button svg,
    [data-testid='stSidebarCollapsedControl'] button span,
    [data-testid='stSidebarNavItems'] button svg,
    section[data-testid='stSidebar'] button svg {
        fill: #333333 !important;
        color: #333333 !important;
    }

    /* Premium Sidebar Background & Design */
    [data-testid='stSidebar'] {
        background: #F0EAD6 !important;
        border-right: 1px solid rgba(0, 0, 0, 0.05) !important;
    }

    /* Global font: Times New Roman, dark color, size 18px */
    html, body, p, div, label, li, a {
        font-family: 'Times New Roman', Times, serif !important;
        color: #333333 !important;
        font-size: 18px !important;
    }

    /* Fix dropdown list text color (make it dark on white background) */
    div[data-baseweb="popover"] div, 
    div[data-baseweb="popover"] span,
    ul[role="listbox"] li, 
    ul[role="listbox"] span {
        color: #0a1628 !important;
    }

    /* Metric cards premium styling (Light Theme) */
    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.6);
        border: 1px solid rgba(0, 0, 0, 0.1);
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        backdrop-filter: blur(10px);
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
student_df = pd.DataFrame({
    "Student Name": ["Dara", "Sophea", "Vuthy", "Malis", "Rithy", "Sreyneang", "Chan", "Bopha"],
    "Course": ["Python", "Statistics", "Python", "Database", "Web App", "Database", "Python", "Statistics"],
    "Score": [85, 68, 45, 92, 58, 91, 72, 62],
    "Attendance": [90, 75, 50, 95, 60, 94, 80, 88],
    "Study Hours": [12, 8, 3, 15, 5, 14, 9, 7],
})

# Step 4: Add a risk levels function ---
def get_risk_level(score, attendance):
    if score < 60 or attendance < 60:
        return "High Risk"
    elif score < 75 or attendance < 75:
        return "Medium Risk"
    else:
        return "Low Risk"

# Step 5: Add a risk levels column ---
student_df["Risk Level"] = student_df.apply(
    lambda row: get_risk_level(row["Score"], row["Attendance"]),
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

# Step 7: Sidebar Navigation ---
with st.sidebar:
    selected_page = option_menu(
        menu_title="EduRisk",
        options=["Home", "Dashboard", "Student Data", "Risk Checker", "About"],
        icons=["house", "speedometer2", "table", "shield-check", "info-circle"],
        menu_icon="mortarboard",
        default_index=0,
        styles={
            "container": {"padding": "15px", "background-color": "rgba(255, 255, 255, 0.5)", "border-radius": "10px", "border": "1px solid rgba(0,0,0,0.1)"},
            "icon": {"color": "#333333", "font-size": "18px"}, 
            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "margin-bottom": "5px", "--hover-color": "rgba(255,255,255,0.8)", "color": "#333333"},
            "nav-link-selected": {"background-color": "white", "color": "#333333", "font-weight": "bold", "box-shadow": "0 2px 5px rgba(0,0,0,0.05)"},
            "menu-title": {"color": "#333333", "font-weight": "bold", "font-size": "22px", "padding-bottom": "15px"}
        }
    )

# Step 8: Home Page ---
if selected_page == "Home":
    st.title("🎓 EduRisk Analytics")
    st.subheader("Interactive Student Risk Monitoring Dashboard")
    st.write("Welcome to Lab 02.")
    st.write("In this lab, you will use Streamlit widgets to explore student performance data.")
    st.success("Lab 02 app is running successfully!")

# -- Step 24: Update the Student Data Page
elif selected_page == "Student Data":
    st.title("Student Data")

    total_students = len(student_df)
    average_score = student_df["Score"].mean()
    average_attendance = student_df["Attendance"].mean()
    high_risk_students = student_df[
        student_df["Risk Level"] == "High Risk"
    ].shape[0]

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Students", total_students)

    with col2:
        st.metric("Average Score", round(average_score, 2))

    with col3:
        st.metric("Average Attendance", f"{round(average_attendance, 2)}%")

    with col4:
        st.metric("High Risk Students", high_risk_students)

    st.subheader("Full Student Dataset")
    styled_df = student_df.style.map(highlight_risk, subset=["Risk Level"])
    st.dataframe(styled_df)

# -- Step 25: Create the Risk Checker Page
elif selected_page == "Risk Checker":
    st.title("Single Student Risk Checker")

    with st.form("risk_checker_form"):
        input_name = st.text_input("Student Name")
        input_score = st.number_input("Score", 0, 100, 50)
        input_attendance = st.number_input("Attendance", 0, 100, 50)
        submitted = st.form_submit_button("Check Risk")

    if submitted:
        risk_result = get_risk_level(input_score, input_attendance)

        st.write("Student Name:", input_name)
        st.write("Score:", input_score)
        st.write("Attendance:", input_attendance)

        if risk_result == "Low Risk":
            st.success("Risk Level: Low Risk")
        elif risk_result == "Medium Risk":
            st.warning("Risk Level: Medium Risk")
        else:
            st.error("Risk Level: High Risk")

# Step 9: Dashboard Page
elif selected_page == "Dashboard":
    st.title("Interactive Dashboard")

    st.write("Use the filters below to explore student performance.")

    with st.container():
        st.markdown("### 🎛️ Filter Options")
        filter_col1, filter_col2 = st.columns(2)
        
        with filter_col1:
            # Step 10: Add Course Filter
            selected_course = st.selectbox(
                "Select Course",
                ["All"] + list(student_df["Course"].unique())
            )
            # Step 12: Add Minimum Attendance Slider
            min_attendance = st.slider(
                "Minimum Attendance (%)",
                0, 100, 0
            )
            
        with filter_col2:
            # Step 11: Add Risk Level Filter
            selected_risk = st.selectbox(
                "Select Risk Level",
                ["All", "Low Risk", "Medium Risk", "High Risk"]
            )
            # Step 13: Add Minimum Score Slider
            min_score = st.slider(
                "Minimum Score",
                0, 100, 0
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # Step 14: Add Filtering Logic
    filtered_df = student_df.copy()

    if selected_course != "All":
        filtered_df = filtered_df[filtered_df["Course"] == selected_course]

    if selected_risk != "All":
        filtered_df = filtered_df[filtered_df["Risk Level"] == selected_risk]

    filtered_df = filtered_df[
        filtered_df["Attendance"] >= min_attendance
    ]

    filtered_df = filtered_df[
        filtered_df["Score"] >= min_score
    ]

    # Step 15: Add Dashboard Metrics
    total_students = len(filtered_df)

    if len(filtered_df) > 0:
        average_score = filtered_df["Score"].mean()
        average_attendance = filtered_df["Attendance"].mean()
    else:
        average_score = 0
        average_attendance = 0

    high_risk_students = filtered_df[
        filtered_df["Risk Level"] == "High Risk"
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

# -- Step 20: Add Show or Hide Dataset Checkbox
    show_data = st.checkbox("Show Filtered Dataset", True)

    if show_data:
        st.subheader("Filtered Student Dataset")
        styled_filtered = filtered_df.style.map(highlight_risk, subset=["Risk Level"])
        st.dataframe(styled_filtered)
    else: 

# -- Step 21: Add Download Button
        st.info("Filtered dataset is hidden.") 
        csv = filtered_df.to_csv(index=False)

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

        if len(filtered_df) > 0:
            fig_score = px.bar(
                filtered_df,
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
                showlegend=False,
                margin=dict(t=30, b=40, l=40, r=20)
            )
            fig_score.update_traces(textposition="outside")
            st.plotly_chart(fig_score, use_container_width=True)
        else:
            st.warning("No data available for score chart.") 

# -- Step 23: Add Risk Level Count Chart
    with chart_col2:
        st.write("Risk Level Count")

        if len(filtered_df) > 0:
            risk_count = filtered_df["Risk Level"].value_counts().reset_index()
            risk_count.columns = ["Risk Level", "Count"]
            fig_risk = px.bar(
                risk_count,
                x="Risk Level",
                y="Count",
                color="Risk Level",
                color_discrete_map=risk_color_map,
                text="Count"
            )
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
    st.write("This app is part of Lab 02.")
    st.write("Course: Web App Development for Data Science")
    st.write("Project Theme: EduRisk Analytics")
    st.write("Topic: Streamlit Interactive Dashboard")
    st.info("Ethics Reminder: Risk prediction should support students, not punish them.")
