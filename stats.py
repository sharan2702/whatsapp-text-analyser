from nltk.corpus import stopwords
from numpy import select
from urlextract import URLExtract
from collections import Counter
from wordcloud import WordCloud
import pandas as pd
import emoji
import nltk
nltk.download('stopwords')

extract = URLExtract()


def fetchstats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]
    num_messages = df.shape[0]
    words = []
    for message in df['Messages']:
        words.extend(message.split())

    mediaomitted = df[df['Messages'] == '<Media omitted>']

    links = []
    for message in df['Messages']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words), mediaomitted.shape[0], len(links)


def fetchbusyuser(df):
    df = df[df['User'] != 'Group Notification']
    count = df['User'].value_counts().head()
    new_df = pd.DataFrame((df['User'].value_counts()/df.shape[0])*100)
    return count, new_df


def createwordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    wc = WordCloud(width=500, height=500, min_font_size=10,
                   background_color='white')

    df_wc = wc.generate(df['Messages'].str.cat(sep=' '))

    return df_wc


def getcommonwords(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]
    temp = df[(df['User'] != 'Group Notification') |
              (df['User'] != '<Media omitted>')]
    words = []

    for message in temp['Messages']:
        for word in message.lower().split():
            if word not in stopwords.words('english'):
                words.append(word)
    mostcommon = pd.DataFrame(Counter(words).most_common(25))

    return mostcommon


def getemojistats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]
    emojis = []

    for message in df['Messages']:
        emojis.extend(
            [c for c in message if c in emoji.distinct_emoji_list(message)])
    emojidf = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emojidf


def monthtimeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]
    temp = df.groupby(['Year', 'Month_num', 'Month']).count()[
        'Messages'].reset_index()

    time = []

    for i in range(temp.shape[0]):
        time.append(temp['Month'][i]+'-'+str(temp['Year'][i]))
    temp['Time'] = time

    return temp


def monthactivitymap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]
    return df['Month'].value_counts()


def weekactivitymap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]
    return df['Day_name'].value_counts()
