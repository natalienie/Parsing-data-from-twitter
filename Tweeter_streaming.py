

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import nltk
from nltk.tokenize import word_tokenize
import pickle


pickle_in_c = open('pickled_MNB_classifier.pickle', 'rb')
MNB_classifier = pickle.load(pickle_in_c)

pickle_in_f = open('pickled_algo_features.pickle', 'rb')
word_features = pickle.load(pickle_in_f)
#import sentiment_mod as s

atoken = '905597828067713029-p0KGaME880KJZYLRqKvp5aoMz1uLRSi'
asecret = 'liKeuuB8EdM7np8z7HTzX6eoFFFz1qsBDmTDwgYTbH9r7'
ckey = 'jE4QX8vY0HFPUZMw3KiHMni6v'
csecret = 'rdf5xMC28AFYKtETSfKiFN4mRQAdi5xKR95SA8K8YxIVkX6weS'

def find_features(document):
    words = word_tokenize(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)
    return features

def sentiment(text):
    feats = find_features(text)
    return MNB_classifier.classify(feats)

class listener(StreamListener):

    def on_data(self, data):

        all_data = json.loads(data)
        tweet = all_data['text']
        print(tweet)
        sentiment_value = sentiment(tweet)

        output = open('twitter_stream_GM.txt', 'a')
        output.write(sentiment_value)
        output.write('\n')
        output.close()

        return True



    def on_error(self, status):
        print(status)

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())
twitterStream.filter(track=['GeneralMills'], languages=['en'])
