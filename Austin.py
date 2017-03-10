import pandas as pd
import numpy as np
import sqlite3
from sqlalchemy import create_engine
import datetime
import tweepy
import time

def save_game(df,overwrite = "none",append = False):
    """Saves Pandas Dataframe to sqlite database. Takes in Pandas Dataframe and name of database(optional). Defualt name is the date."""
    if overwrite != "none":
        engine = create_engine('sqlite:///'+overwrite+'.sqlite')
        if  append == True:
            df.to_sql('table',engine,if_exists='append')
        else:
            df.to_sql('table',engine,if_exists='replace')
            print "You have succesfully saved!"
        return
    else :
        name = str(datetime.datetime.now().date()).replace(" ","").replace("-","").replace(":","").replace(".","")
        enginename = 'sqlite:///%s.sqlite' % name
        engine = create_engine(enginename)
        if append == True:
            df.to_sql('table',engine,if_exists='append')
        else:
            df.to_sql('table',engine,if_exists='replace')
            print "You have succesfully saved!"
        return






class Auth(object):
    def __init__(self):
        self.API_KEY = 	"9AVB69rIkU9mwFxkOxM8hfy1t"
        self.API_SECRET = "rhJU9HuvHAaMAoYDgbkwKuJlTnooEcGDbvQVzJfjlSMCmGzOKR"
        self.TWITTER_KEY = "24664791-skDfYfQUIacKDRnQotU76OQ7bqz3pl1osCXt4L2oq"
        self.TWITTER_SECRET = "rE5t774BYTOZlherSqxmwkRZPqk3M3rkuLcRufdxNbFBL"






    

class StreamSaver(tweepy.StreamListener):
    def on_status(self, status):
        temp = {"User" : status.user.screen_name,"Text" : status.text,"Coord" : status.coordinates,"Time" : status.created_at}
        tempdf = pd.DataFrame([temp])
        print tempdf
        save_game(tempdf,append = True,overwrite = "Twitter")
        
        
    
    
    def on_error(self, status_code):
        if status_code == 420:
            return False
        



def createconnectiontostreamer(a):
    """a is an Auth() object"""
    auth = tweepy.OAuthHandler(a.API_KEY, a.API_SECRET)
    auth.set_access_token(a.TWITTER_KEY, a.TWITTER_SECRET)
    api = tweepy.API(auth)
    stream_saver = StreamSaver()
    stream = tweepy.Stream(auth = api.auth, listener = stream_saver)
    return stream


def streamrestarter(a,listofsearch = ["muslim ban","travel ban"]):
    """a is auth object (get from createconnectiontostreamer()), listofsearch is list of search terms. """
    
    try:
        createconnectiontostreamer(a).filter(track=listofsearch)
        return
    except KeyboardInterrupt:
        createconnectiontostreamer(a).disconnect()
        return
    except:
        time.sleep(5)
        print "ERROR! RESTARTING!"
        streamrestarter(a,listofsearch)
        return

