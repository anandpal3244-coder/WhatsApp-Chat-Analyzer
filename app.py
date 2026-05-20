import streamlit as st
import helper
import preprocessor as pp
import pandas as pd
import plotly.express as px

# ---------- BACKGROUND STYLE ----------
def set_bg():

    page_bg = """
    <style>

    /* Main App Background */
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1557683316-973673baf926");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: rgba(0,0,0,0.75);
        backdrop-filter: blur(10px);
    }

    /* Cards / Containers */
    .block-container {
        background: rgba(255,255,255,0.08);
        padding: 2rem;
        border-radius: 15px;
        backdrop-filter: blur(12px);
    }

    /* Text Color */
    h1, h2, h3, h4, h5, h6, p, label {
        color: white !important;
    }

    </style>
    """

    st.markdown(page_bg, unsafe_allow_html=True)

set_bg()
# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="WhatsApp Chat Analyzer",
    page_icon="💬",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.big-font {
    font-size:22px !important;
    font-weight:bold;
}
.metric-card {
    background-color:#0e1117;
    padding:20px;
    border-radius:10px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.title("💬 WhatsApp Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Upload WhatsApp Chat")

# ---------------- LOAD DATA ----------------
if uploaded_file is not None:

    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = pp.preprocessor(data)

    # User List
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "overall")

    selected_user = st.sidebar.selectbox(
        "Select User",
        user_list
    )

    if st.sidebar.button("🚀 Analyze Chat"):

        # ================= KPI SECTION =================
        st.title("📊 WhatsApp Chat Dashboard")

        num_messages, words, media, links = helper.fetch_stats(selected_user, df)

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total Messages", num_messages)
        col2.metric("Total Words", words)
        col3.metric("Media Shared", media)
        col4.metric("Links Shared", links)

        st.divider()

        # ================= TIMELINE =================
        st.subheader("📈 Monthly Timeline")

        timeline = helper.monthly_timeline(selected_user, df)

        fig = px.line(
            timeline,
            x="time",
            y="message",
            markers=True,
            title="Message Trend Over Time"
        )

        st.plotly_chart(fig, use_container_width=True)

        # ================= DAILY ACTIVITY =================
        st.subheader("📅 Daily Activity")

        daily = helper.daily_timeline(selected_user, df)

        fig = px.line(
            daily,
            x="only_date",
            y="message",
            title="Daily Messages"
        )

        st.plotly_chart(fig, use_container_width=True)

        # ================= BUSY USERS =================
        if selected_user == "overall":

            st.subheader("🔥 Most Active Users")

            x, new_df = helper.most_busy_users(df)

            fig = px.bar(
                x,
                x=x.index,
                y=x.values,
                labels={'x': 'User', 'y': 'Messages'}
            )

            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(new_df)

        # ================= WORD ANALYSIS =================
        st.subheader("📝 Most Common Words")

        common_words = helper.most_common_words(selected_user, df)

        fig = px.bar(
            common_words,
            x=0,
            y=1,
            title="Top Words Used"
        )

        st.plotly_chart(fig, use_container_width=True)

        # ================= EMOJI ANALYSIS =================
        st.subheader("😂 Emoji Analysis")

        emoji_df = helper.emoji_helper(selected_user, df)

        fig = px.pie(
            emoji_df.head(10),
            values=1,
            names=0,
            title="Top Emojis"
        )

        st.plotly_chart(fig, use_container_width=True)

        # ================= ACTIVITY MAP =================
        st.subheader("📊 Activity Map")

        col1, col2 = st.columns(2)

        with col1:
            busy_day = helper.week_activity_map(selected_user, df)
            fig = px.bar(
                busy_day,
                title="Most Busy Day"
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            busy_month = helper.month_activity_map(selected_user, df)
            fig = px.bar(
                busy_month,
                title="Most Busy Month"
            )
            st.plotly_chart(fig, use_container_width=True)

        # ================= HEATMAP =================
        st.subheader("🕒 Online Activity Heatmap")

        heatmap = helper.activity_heatmap(selected_user, df)

        fig = px.imshow(
            heatmap,
            color_continuous_scale="Blues",
            aspect="auto"
        )

        st.plotly_chart(fig, use_container_width=True)