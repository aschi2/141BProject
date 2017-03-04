import pandas as pd
import numpy as np
import sqlite3
from sqlalchemy import create_engine
import datetime

def save_game(df,overwrite = "none"):
    if overwrite != "none":
        engine = create_engine('sqlite:///'+overwrite+'.sqlite')
        df.to_sql('table',engine,if_exists='replace')
        print "You have succesfully saved!"
    else :
        name = str(datetime.datetime.now()).replace(" ","").replace("-","").replace(":","").replace(".","")
        enginename = 'sqlite:///%s' % name
        dayname = enginename[:18] + '.sqlite'
        engine = create_engine(dayname)
        df.to_sql('table',engine,if_exists='replace')
        print "You have succesfully saved!"