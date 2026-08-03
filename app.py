import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================
# Page Settings
# ==========================
st.set_page_config(
    page_title="Academic & Sleep Dashboard",
    layout="wide"
)

st.title("🎓 Student Sleep Pattern & Academic Performance Dashboard")
st.markdown("Analyze the relationship between sleep habits and academic performance.")

# ==========================
# Load Data
# ==========================
@st.cache_data
def load_data():
    df = pd.read_csv("college_sleep_and_gpa.csv")

    # Cleaning
    df = df.dropna(subset=["gender"]).reset_index(drop=True)

    df["first_generation"] = df["first_generation"].fillna(-1)
    df["underrepresented"] = df["underrepresented"].fillna(-1)

    df.loc[df["first_generation"] == 2.0, "first_generation"] = -1

    df = df.dropna(subset=["term_units", "term_load_z"]).reset_index(drop=True)

    df = df.drop_duplicates(subset=["study", "student_id"], keep="first")

    return df


df = load_data()

# ==========================
# KPIs
# ==========================
st.subheader("📊 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

avg_sleep = df["avg_sleep_hours"].mean()
avg_gpa = df["term_gpa"].mean()
under6 = (df["under_6h_sleep"].sum() / len(df)) * 100
students = len(df)

col1.metric("Total Students 🧑‍🎓", students)
col2.metric("Average Sleep 💤", f"{avg_sleep:.2f} hrs")
col3.metric("Average GPA 🎓", f"{avg_gpa:.2f}")
col4.metric("Sleep < 6h Ratio ⌚", f"{under6:.1f}%")

st.divider()

# ==========================
# Scatter + Boxplot
# ==========================
st.subheader("💤 Sleep vs Academic Performance")

c1, c2 = st.columns(2)

with c1:
    fig = px.scatter(
        df,
        x="avg_sleep_hours",
        y="term_gpa",
        title="Sleep Hours vs GPA",
        color_discrete_sequence=["darkmagenta"],
        opacity=0.7
    )
    fig.update_traces(marker_size=9)
    st.plotly_chart(fig, use_container_width=True)

with c2:

    sleep_order = [
        "<5.5h",
        "5.5-6h",
        "6-6.5h",
        "6.5-7h",
        "7-7.5h",
        "7.5h+"
    ]

    fig = px.box(
        df,
        x="sleep_bracket",
        y="term_gpa",
        category_orders={"sleep_bracket": sleep_order},
        title="GPA by Sleep Bracket",
        color_discrete_sequence=["mediumvioletred"]
    )

    st.plotly_chart(fig, use_container_width=True)

st.divider()

# ==========================
# Second Row
# ==========================
st.subheader("🏫 Demographic Insights")

c1, c2, c3 = st.columns(3)

with c1:

    temp = (
        df.groupby("under_6h_sleep")["term_gpa"]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        temp,
        x="under_6h_sleep",
        y="term_gpa",
        title="Average GPA by Under 6h Sleep",
        color_discrete_sequence=["#FCE2E3"]
    )

    st.plotly_chart(fig, use_container_width=True)

with c2:

    fig = px.histogram(
        df,
        x="gender",
        color="sleep_bracket",
        barmode="group",
        category_orders={"sleep_bracket": sleep_order},
        color_discrete_sequence=px.colors.sequential.RdPu,
        title="Gender & Sleep Bracket"
    )

    st.plotly_chart(fig, use_container_width=True)

with c3:

    fig = px.box(
        df,
        x="university",
        y="term_gpa",
        color_discrete_sequence=["darkmagenta"],
        title="GPA by University"
    )

    fig.update_layout(xaxis_tickangle=-20)

    st.plotly_chart(fig, use_container_width=True)

st.divider()

# ==========================
# Bottom Charts
# ==========================
st.subheader("📈 Distribution & Correlation")

c1, c2 = st.columns(2)

with c1:

    fig = px.histogram(
        df,
        x="avg_sleep_hours",
        nbins=25,
        title="Sleep Hours Distribution",
        color_discrete_sequence=["#F6BEB9"]
    )

    st.plotly_chart(fig, use_container_width=True)

with c2:

    fig = px.pie(
        df,
        names="university",
        hole=0.6,
        color_discrete_sequence=px.colors.sequential.RdPu,
        title="University Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)


st.divider()

st.success("Dashboard Loaded Successfully ✅")
