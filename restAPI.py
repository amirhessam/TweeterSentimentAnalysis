from flask import Flask
from flask_restful import Resource, Api, reqparse

class Accounts(Resource):
    def __init__(self, data):
        self.data = data
    def get(self):
        # return list of all accounts
        return self.data.query("reply == False").username.unique().tolist()

class Tweets(Resource):
    def __init__(self, data):
        self.data = data
    def get(self, username):
        main_tweets = self.data.query("reply == False and username == \"{}\"".format(username))
        out = []
        for index, t in main_tweets.iterrows():
            d = dict()
            d['content'] = t['content']
            d['date'] = str(t['date'])
            d['retweetCount'] = t['retweetCount']
            d['replyCount'] = t['replyCount']
            d['likeCount'] = t['likeCount']
            d['viewCount'] = t['viewCount']
            d['replies'] = self.data.query("reply == True and conversationId == " + str(t.conversationId))[
                ['content', 'username', 'date', 'retweetCount', 'replyCount', 'likeCount', 'viewCount']].to_json(
                index=False, orient='split', force_ascii=False)
            out.append(d)
        return out#return list of conversation threads since start

class Audience(Resource):
    def __init__(self, data):
        self.data = data
    def get(self, username):
        main_tweets = self.data.query("reply == False and username == \"{}\"".format(username))
        out = []
        for index, t in main_tweets.iterrows():
            out += self.data.query("reply == True and conversationId == " + str(t.conversationId)).username.unique().tolist()
        return list(set(out))#return information about audiance

class Sentiment(Resource):
    def __init__(self, data):
        self.data = data
    def get(self, username):
        main_tweets = self.data.query("reply == False and username == \"{}\"".format(username))
        out = []
        for index, t in main_tweets.iterrows():
            d = dict()
            d['content'] = t['content']
            d['date'] = str(t['date'])
            d['sentiment'] = t['sentiment']
            d['replies'] = self.data.query("reply == True and conversationId == " + str(t.conversationId))[
                ['content', 'username', 'date', 'sentiment']].to_json(
                index=False, orient='split', force_ascii=False)
            out.append(d)
        return out#return sentiment thread level/audiance level

class ToyAPI:
    def __init__(self, data):
        self.data = data
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.api.add_resource(Accounts, '/accounts', resource_class_kwargs={'data': self.data})
        self.api.add_resource(Tweets, '/tweets/<string:username>', resource_class_kwargs={'data': self.data})
        self.api.add_resource(Audience, '/audience/<string:username>', resource_class_kwargs={'data': self.data})
        self.api.add_resource(Sentiment, '/sentiment/<string:username>', resource_class_kwargs={'data': self.data})
    def start(self):
        try:
            self.app.run()
        except Exception as e:
            print(e)


