import re
import pandas as pd

def preprocess(data):
    # Define the pattern for message timestamps
    pattern = r'\d{1,2}/\d{1,2}/\d{2}, \d{1,2}:\d{2}\s?[AP]M -'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    dates = [date.replace('\u202f', ' ') for date in dates]

    # Create DataFrame
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    # Clean and convert date strings
    df['message_date'] = df['message_date'].str.strip().str.rstrip('-').str.strip()
    df['message_date'] = pd.to_datetime(df['message_date'], format='%m/%d/%y, %I:%M %p')
    df.rename(columns={'message_date': 'date'}, inplace=True)
    
    # Separate Username and Messages
    users, messages = [], []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])
    
    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)
    
    # Extract additional date features
    df['t_dates'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['month_num'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['day_name'] = df['date'].dt.day_name()
    
    # Define time periods
    period = []
    for hour in df['hour']:
        if hour == 23:
            period.append(f"{hour}-00")
        elif hour == 0:
            period.append(f"00-{hour + 1}")
        else:
            period.append(f"{hour}-{hour + 1}")
    
    df['period'] = period
    return df

