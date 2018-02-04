import json
import tweepy
import config as cfg
from pymongo import MongoClient

MONGO_DB = 'mongodb://localhost:27017/'

USERS = [
    'smartdissent', 'SparkleSoup45', 'bbusa617', 'charlieJuliet', 'ChrisFromWI',
    'SCroixFreePress', 'wienerherzog2', 'PeggyRuppe', 'remleona', 'Answers2b4u',
    'veradubs', 'HarryFerro', 'RussiaInsider', 'Rose4Justice', 'ChristTopNews',
    'actionScript3', 'willie_c', 'FilAmVA', 'pnehlen', 'Russ_Warrior', 'palestininianpr',
    '501Wittmann', 'TexanTruth42', 'VNLP2', 'elapoides', 'K1erry', 'justshootme_plz',
    'starrick1', 'RoseGeorossi', 'MaineFirstMedia', 'Axis__Mundi', 'Imperator_Rex3',
    'fcfootsteps', 'TrumpArmyDawn', 'TT45pac', 'AMErikaNGIRLBOT', 'gal_deplorable',
    'bdcousins', 'k_ovfefe', 'drawandstrike', 'antischool_ftw', 'B75434425', 'PatsforTruth',
    'MollyBly', 'anarcho_commie', 'Mathew_Foresta', 'zalphaprime', 'booatticus63',
    'USA_H8S_ANTIFA', 'hauzer76', 'SONOFDY1', 'DeceitinDrugs', 'DANEgerus',
]

KEYWORDS = [
    'MAGA', 'ReleaseTheMemo', 'Nunes'
]

class TweetListener(tweepy.StreamListener):
    '''
    Class that provides listening services to Twitter Streaming API
    '''
    def __init__(self, api):
        '''
        Initialize Stream Listener Service and connect to DB
        '''
        self.api = api
        super(tweepy.StreamListener, self).__init__()
        self.db = MongoClient().twitter

    def on_data(self, tweet):
        '''
        Save JSON data to DB
        '''
        json_data = json.loads(tweet)
        print("Tweet stored at " + json_data['created_at'])
        self.db.tweet.insert(json_data)

    def on_connect(self):
        '''
        Declare proper connection to DB
        '''
        print("You are now connected to the streaming API.")

    def on_error(self, status_code):
        '''
        Declare error when encountered, do not close stream
        '''
        print("Error with code: " + str(status_code))
        return True

    def on_timeout(self):
        '''
        Declare API timeout when encountered, do not close stream
        '''
        print("API Timeout")
        return True

def get_user_ids(api, usernames):
    '''
    Function to return array of User IDs corresponding to Usernames in USERS
    '''
    result = []
    for username in usernames:
        try:
            user = api.get_user(screen_name = username)
            user_id = user.id
            result.append(user_id)
        except tweepy.error.TweepError:
            pass
    return result



def main():
    # Authenticate with Twitter API
    auth = tweepy.OAuthHandler(cfg.API_KEY, cfg.API_SECRET)
    auth.set_access_token(cfg.ACCESS_TOKEN, cfg.ACCESS_SECRET)
    api = tweepy.API(auth)

    # get User IDs from usernames in USERS array
    # user_ids = get_user_ids(api, USERS)

    # Setup Listener
    listener = tweepy.Stream(auth, TweetListener(api))

    # Track tweets from USERS and KEYWORDS
    # listener.filter(follow = USERS, track = KEYWORDS)
    listener.filter(track = KEYWORDS)
    # listener.filter(follow = USERS)

if __name__ == "__main__":
    main()
