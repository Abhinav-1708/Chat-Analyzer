from urlextract import URLExtract
import pandas as pd
import emoji
from collections import Counter
from wordcloud import WordCloud

extract = URLExtract()

# Fetch user statistics
def fetch_stats(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    
    num_messages = df.shape[0]
    words = [word for message in df['message'] for word in message.split()]
    num_media_message = df[df['message'] == '<Media omitted>\n'].shape[0]
    links = [link for message in df['message'] for link in extract.find_urls(message)]
    
    return num_messages, len(words), num_media_message, len(links)

# Get the most active users
def most_active_user(df):
    df = df[df['user'] != 'group_notification']
    x = df['user'].value_counts().head()
    
    df_activity = (df['user'].value_counts() / df.shape[0]) * 100
    df_activity = df_activity.reset_index()
    df_activity.columns = ['name', 'percent']
    
    return x, df_activity

# Create a word cloud
def create_wordcloud(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    
    with open('stop_hinglish.txt', 'r', encoding='utf-8') as f:
        stop_words = set(f.read().splitlines())
    
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    
    def remove_stop_words(message):
        return " ".join(word for word in message.lower().split() if word not in stop_words)
    
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

# Most common words
def most_common_words(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    
    with open('stop_hinglish.txt', 'r', encoding='utf-8') as f:
        stop_words = set(f.read().splitlines())
    
    with open('emojis.txt', 'r', encoding='utf-8') as f:
        emojis = set(f.read().splitlines())
    
    words = [word for message in temp['message'] for word in message.lower().split() if word not in stop_words and word not in emojis]
    
    return_df = pd.DataFrame(Counter(words).most_common(20))
    return return_df

# Emoji analysis
def emoji_helper(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    
    emojis = [c for message in df['message'] for c in message if emoji.is_emoji(c)]
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

# Monthly and daily timelines
def timeline_monthly(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    timeline["time"] = timeline['month'] + "-" + timeline['year'].astype(str)
    return timeline

def daily_timeline(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    
    d_timeline = df.groupby(['t_dates']).count()['message'].reset_index()
    return d_timeline

# Weekly and monthly activity
def week_activity(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    return df['day_name'].value_counts()

def month_activity(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    return df['month'].value_counts()

# Heatmap
def activity_heatmap(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    act_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
    return act_heatmap

