import json
import tweepy
import config as cfg
from pymongo import MongoClient
from retry import retry

MONGO_DB = 'mongodb://localhost:27017/'

KEYWORDS_PATH = "data/keywords.txt"
USERS_PATH = "data/users.txt"

USERS = [
    'smartdissent', 'SparkleSoup45', 'bbusa617', 'charlieJuliet', 'ChrisFromWI',
    'SCroixFreePress', 'wienerherzog2', 'PeggyRuppe', 'remleona', 'Answers2b4u',
    'veradubs', 'HarryFerro', 'Rose3Justice', 'ChristTopNews',
    'actionScript3', 'willie_c', 'FilAmVA', 'pnehlen', 'Russ_Warrior', 'palestininianpr',
    '501Wittmann', 'TexanTruth42', 'VNLP2', 'elapoides', 'K1erry', 'justshootme_plz',
    'starrick1', 'RoseGeorossi', 'MaineFirstMedia', 'Axis__Mundi', 'Imperator_Rex3',
    'fcfootsteps', 'TrumpArmyDawn', 'TT45pac', 'AMErikaNGIRLBOT', 'gal_deplorable',
    'bdcousins', 'k_ovfefe', 'drawandstrike', 'antischool_ftw', 'B75434425', 'PatsforTruth',
    'MollyBly', 'anarcho_commie', 'Mathew_Foresta', 'zalphaprime', 'booatticus63',
    'USA_H8S_ANTIFA', 'hauzer76', 'SONOFDY1', 'DeceitinDrugs', 'DANEgerus',
]

KEYWORDS = [
    'MAGA', 'ReleaseTheMemo', 'Nunes', 'Mueller', 'Deep State', 'Flynn',
    'Obama', 'Deplorable',
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
        try:
            json_data = json.loads(tweet)
            self.db.tweet.insert(json_data)
        except:
            pass

    def on_connect(self):
        '''
        Declare proper connection to API
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


def read_from_textfile(filepath):
    '''
    Function that reads textfiles and returns array of values
    '''
    return [line.rstrip('\n') for line in open(filepath)]

def write_to_textfile(filepath, value_array):
    '''
    Function that accepts an array of values and write to a new textfile line-by-line
    If the textfile already exists, you'll want to use `append_to_textfile` instead
    '''
    with open(filepath, 'w') as file:
        for value in value_array:
            file.write('{}\n'.format(value))

def append_to_textfile(filepath, value_array):
    '''
    Function that accepts an array of values and appends them to existing textfile
    '''
    with open(filepath, 'a') as file:
        for value in value_array:
            file.write('{}\n'.format(value))

def convert_username_to_userid(api, filename, usernames):
    '''
    Function that accepts an array of usernames and appends found user ids to
    the supplied filename
    '''
    result = []
    for username in usernames:
        try:
            user = api.get_user(screen_name = username)
            user_id = user.id
            result.append(user_id)
        except tweepy.error.TweepError:
            pass
    append_to_textfile(filename, result)


@retry(delay = 60, backoff = 30, max_delay = 600)
def main():
    # Authenticate with Twitter API
    auth = tweepy.OAuthHandler(cfg.API_KEY, cfg.API_SECRET)
    auth.set_access_token(cfg.ACCESS_TOKEN, cfg.ACCESS_SECRET)
    api = tweepy.API(auth)

    # Convert usernames to user ids and store in textfile
    # convert_username_to_userid(api, USERS_PATH, USERS)

    user_list = read_from_textfile(USERS_PATH)
    keywords_list = read_from_textfile(KEYWORDS_PATH)

    # Setup Listener
    listener = tweepy.Stream(auth, TweetListener(api))
    # Track tweets from USERS and KEYWORDS
    listener.filter(follow = user_list, track = keywords_list, stall_warnings = True)

if __name__ == "__main__":
    main()
