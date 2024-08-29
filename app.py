import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# Sidebar configuration
st.sidebar.title("WhatsApp Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:
    # Read and preprocess data
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    # Fetch unique users and sort
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")
    
    selected_user = st.sidebar.selectbox("Select User", user_list)
    
    if st.sidebar.button("Show Analytics"):
        # Display statistics
        st.title("TOP STATISTICS")
        num_messages, words, num_media_message, num_links = helper.fetch_stats(selected_user, df)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header("Total Messages")
            st.subheader(num_messages)
        with col2:
            st.header("Total Words")
            st.subheader(words)
        with col3:
            st.header("Total Media Items")
            st.subheader(num_media_message)
        with col4:
            st.header("Links Shared")
            st.subheader(num_links)
        
        # Display timelines
        st.title("Timelines")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Monthly Timeline")
            timeline = helper.timeline_monthly(selected_user, df)
            fig, ax = plt.subplots()
            ax.plot(timeline['time'], timeline['message'], color='red')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.subheader("Daily Timeline")
            d_timeline = helper.daily_timeline(selected_user, df)
            fig, ax = plt.subplots()
            ax.plot(d_timeline['t_dates'], d_timeline['message'], color='green')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        
        # Display activity maps
        st.title("Activity Maps")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Most Busy Day")
            busy_day = helper.week_activity(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.subheader("Most Busy Month")
            busy_month = helper.month_activity(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        
        # Most active users
        if selected_user == "Overall":
            col1, col2 = st.columns(2)
            x, new_df = helper.most_active_user(df)
            fig, ax = plt.subplots()
            with col1:
                st.subheader("Most Active Users")
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)
        
        # WordCloud
        st.title("WordCloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc, interpolation='bilinear')
        ax.axis('off')
        st.pyplot(fig)
        
        # Most common words
        st.title("Most Common Words")
        most_common_df = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        
        # Emoji analysis
        st.title("Most Commonly Used Emojis")
        emoji_df = helper.emoji_helper(selected_user, df)
        st.dataframe(emoji_df)
        
        # Heatmap
        st.title("Weekly Heat Map")
        act_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        sns.heatmap(act_heatmap, ax=ax)
        st.pyplot(fig)
