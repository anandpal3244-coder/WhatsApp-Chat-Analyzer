import streamlit as st
import preprocessor as pp,helper
import matplotlib.pyplot as plt
import seaborn as sns

from helper import most_common_words

st.sidebar.title('Whatsaap Chat Analysis')

uploaded_file = st.sidebar.file_uploader('Upload your file')
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = pp.preprocessor(data)

    st.dataframe(df)

    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,'overall')
    st.subheader('User List')
    selected_user = st.sidebar.selectbox(' Show analysis wrt', user_list)

    if st.sidebar.button('Show Analysis'):

        # ---------- Top Stats ----------
        num_message, word, num_media_msg, num_links = helper.fetch_stats(selected_user, df)

        st.title('Top Statistics of WhatsApp Chat Analysis')

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total Messages", num_message)
        col2.metric("Total Words", word)
        col3.metric("Media Shared", num_media_msg)
        col4.metric("Links Shared", num_links)

        # ---------- Busy Users ----------
        if selected_user == 'overall':
            st.title('Most Busy Users')

            x, new_df = helper.most_busy_users(df)

            col1, col2 = st.columns(2)

            with col1:
                fig, ax = plt.subplots()
                ax.bar(x.index, x.values)
                plt.xticks(rotation=90)
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

        # ---------- Common Words ----------
        st.title('Most Common Words')

        most_common_df = helper.most_common_words(selected_user, df)

        fig, ax = plt.subplots()
        ax.bar(most_common_df[0], most_common_df[1])
        plt.xticks(rotation=90)

        st.pyplot(fig)

        # ---------- Emoji Analysis ----------
        st.title('Emoji Analysis')

        emoji_df = helper.emoji_helper(selected_user, df)

        col1, col2 = st.columns(2)

        col1.dataframe(emoji_df)

        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1], labels=emoji_df[0], autopct='%1.1f%%')
            st.pyplot(fig)

        # ---------- Monthly Timeline ----------
        st.title("Monthly Timeline Analysis")

        timeline = helper.monthly_timeline(selected_user, df)

        fig, ax = plt.subplots()

        ax.plot(timeline['time'], timeline['message'])
        plt.xticks(rotation='vertical')
        plt.show()

        st.pyplot(fig)

        # Daily Timeline

        st.title('Daily Timeline Analysis')
        daily_timeline = helper.daily_timeline(selected_user, df)

        fig, ax = plt.subplots()

        ax.plot(daily_timeline['only_date'], daily_timeline['message'])
        plt.xticks(rotation='vertical')
        plt.show()
        st.pyplot(fig)

        st.title('Activity Map')
        col1, col2 = st.columns(2)

        with col1:
            st.header('Most Busy Day')
            busy_day = helper.week_activity_map (selected_user, df)

            fig, ax = plt.subplots()

            ax.bar(busy_day.index, busy_day.values,color='blue')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)


        with col2:
            st.header('Most Busy Month')
            busy_month = helper.month_activity_map(selected_user, df)

            fig, ax = plt.subplots()

            ax.bar(busy_month.index, busy_month.values, color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)


        st.title('Online Activity Map')
        user_heatmap = helper.activity_heatmap(selected_user,df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)


