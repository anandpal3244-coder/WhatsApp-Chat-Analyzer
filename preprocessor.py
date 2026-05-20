import re
import pandas as pd

def preprocessor(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s?(?:am|pm|AM|PM)\s-\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    df = pd.DataFrame({"user_message": messages, "message_date": dates})
    df['message_date'] = pd.to_datetime(df['message_date'], format="%d/%m/%Y, %I:%M %p - ")
    df.rename(columns={'message_date': 'Date'}, inplace=True)
    users = []
    messages = []

    for message in df['user_message']:

        entry = re.split(r'([^:]+):\s', message)

        if len(entry) > 2:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=["user_message"], inplace=True)
    df['user'] = df['user'].str.replace(r'\+?\d[\d\s-]{8,}', 'User', regex=True)
    df['Day'] = df['Date'].dt.day
    df['day_name'] = df['Date'].dt.day_name()
    df['only_date'] = df['Date'].dt.date
    df['Month'] = df['Date'].dt.month_name()
    df['month_num'] = df['Date'].dt.month
    df['Year'] = df['Date'].dt.year
    df['Hour'] = df['Date'].dt.hour
    df['Minute'] = df['Date'].dt.minute

    period = []

    for hour in df['Hour']:

        if hour == 23:
            period.append(str(hour) + "-00")

        elif hour == 0:
            period.append("00-" + str(hour + 1))

        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df
