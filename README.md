# TwitterSentimentAnalysis
A toy project to fetch tweets and do sentiment analysis


# How to use 

run main.py and it will launch a server on localhost serving the following rest api endpoints

'/accounts' #returning the list of twitter accounts that were tracked

'/tweets/<string:username>' #returning the list of twitts for a given username

'/audience/<string:username>', #returning the list of accounts who replied to the given username

'/sentiment/<string:username>' #returning the list of tweets and their sentiment
