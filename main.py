import pandas as pd
import fetchTweets
import sentiment
import restAPI
import os
account_list = [
    ('elonmusk', 'en'),
    ('alikarimi_ak8', 'fa'),
    ('BarackObama', 'en'),
    ('taylorlorenz', 'en'),
    ('cathiedwood', 'en'),
    ('ylecun', 'en')
]


def get_preliminary_data(reply_limit):
    df_list = []
    ft = fetchTweets.FetchTweets()
    for username, lang in account_list:
        tw_l = ft.get_tweets_for(username, '2023-02-01', '2023-03-10', reply_limit=reply_limit, min_fav = 10)
        df = pd.DataFrame(tw_l, columns=['content', 'username', 'date', 'retweetCount', 'replyCount', 'likeCount', 'viewCount', 'conversationId', 'id', 'reply'])
        df['sentiment'] = 'N/A'
        df['language'] = lang
        df_list.append(df)
    df = pd.concat(df_list, axis=0)
    return df

def set_sentiment(df):
    analyzer = sentiment.SentimentAnalyzer()
    df_persian = df.query('language == "fa"')
    df_english = df.query('language == "en"')
    df_persian['sentiment'] = analyzer.persian_sentiment(list(df_persian['content']))
    df_english['sentiment'] = analyzer.english_sentiment(list(df_english['content']))
    return pd.concat([df_persian, df_english], axis=0)

if __name__ == '__main__':
    if os.path.exists('./tweet_data.csv'):
        df = pd.read_csv('./tweet_data.csv', encoding='utf8')
    else:
        df = get_preliminary_data(20)
        df = set_sentiment(df)
        df.to_csv('./tweet_data.csv', index=False, encoding='utf8')
    api = restAPI.ToyAPI(df)
    api.start()

