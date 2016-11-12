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
        last=j
    starttime=arrow.get(last[1]).to("US/Eastern")
    endtime=arrow.now().to("US/Eastern")
    yield {"content":last[0],"start":int(starttime.timestamp)*1000,"end":int(endtime.timestamp)*1000}


def get_timestamps(i):
    if int(arrow.get(i[0]).timestamp)> 0:
        return arrow.get(i[0]).timestamp 


# written to migrate sqlite to Mongo
def write_HA():
    with db_cursor() as c:
        c.execute("select state,last_changed from states where entity_id='sensor.location' and state!='unknown';")
        l=c.fetchall()
    for i,j in zip(l,l[1:]):
        starttime=arrow.get(i[1])
        endtime=arrow.get(j[1])
        diff=endtime.timestamp-starttime.timestamp
        yield {"User":"Sriram","State":i[0],"Start":int(starttime.timestamp),"End":int(endtime.timestamp),"Diff":diff}


for i in list(write_HA()):
    dbtest.write_location(i)