
from sqlitedict import SqliteDict 


##TODO: put these within a switch 
def register_user(user:str,user_api_key:str):
    with SqliteDict("./users.sqlite") as sqldict:
        sqldict[user] = user_api_key
        sqldict.commit()

def cache_streak(user,streak_data):
    with SqliteDict("./cache.sqlite") as sqldict:
        sqldict[user] = streak_data
        sqldict.commit()

def has_cached_streak(user):
    with SqliteDict("./cache.sqlite") as sqldict:
        if user in sqldict.keys():
            print("Cache hit")
            return sqldict[user]
    return None

def is_user_registered(user:str):
    exists = False
    with  SqliteDict("./users.sqlite") as sqldict:
        exists =  user in sqldict.keys()
    return exists

def get_user_api_key(user:str):
    with  SqliteDict("./users.sqlite") as sqldict:
        return sqldict[user]

def get_registered_users():
    with  SqliteDict("./users.sqlite") as sqldict:
        return list(sqldict.keys())

def deregister_user(username:str):
    with  SqliteDict("./users.sqlite") as sqldict:
        del sqldict[username]
        sqldict.commit()

        

