import sqlite3,datetime
import time
from contextlib import contextmanager
from os import path
from config import DATABASE,arrow
import dbtest


@contextmanager
def db_cursor():
    """ Use this as a context manager and it will automatically
    commit and close the database connection for you."""
    conn = sqlite3.connect(DATABASE)
    yield conn.cursor()
    conn.commit()
    conn.close()

def get_states():
    with db_cursor() as c:
        c.execute("select state,last_changed from states where entity_id='sensor.location' and state!='unknown';")
        l=c.fetchall()    
    for i,j in zip(l,l[1:]):
        starttime=arrow.get(i[1]).to("US/Eastern")
        endtime=arrow.get(j[1]).to("US/Eastern")
        if i[0]!=j[0]:
            yield {"content":i[0],"start":int(starttime.timestamp)*1000,"end":int(endtime.timestamp)*1000}



def get_Data():
  with db_cursor() as c:
        c.execute("select state,last_changed from states where entity_id='sensor.location' and state!='unknown';")
        l=c.fetchall()
  	for i in l:
		starttime=arrow.get(i[1]).to("US/Eastern")
		yield {"user":"sriram","state":i[0],"time":starttime.timestamp}
		

def push_mongo():
    db=get_db()
    c=list(get_Data())
    db.location.insert(c)

def get_timestamps(i):
    if int(arrow.get(i[0]).timestamp)> 0:
        return arrow.get(i[0]).timestamp 
#
# def get_sleep():
#     with db_cursor() as c:
#         c.execute("select state from states where entity_id='sensor.slept' and state!='unknown';")
#         s=list(set(c.fetchall()))
#         sleeplist=list(map(get_timestamps,s))
#         c.execute("select state from states where entity_id='sensor.woke_up' and state!='unknown';")
#         w=list(set(c.fetchall()))
#         wokelist=list(map(get_timestamps,w))
#         sleeplist=list(filter(lambda x:x!=None or x<0,sleeplist))
#         wokelist=list(filter(lambda x:x!=None or x<0,wokelist))
#         print len(sleeplist),len(wokelist)
#         for i,j in zip(sorted(sleeplist),sorted(wokelist)):
#             yield {"user":"sriram","slept":i,"woke":j,"duration":int(j-i)}
#             x=i
#             y=j
#         print arrow.get(x).format("MM-DD-YY HH:mm")
#
# for i in list(get_Data()):
#     print i
