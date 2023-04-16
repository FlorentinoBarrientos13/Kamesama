
from sqlitedict import SqliteDict 


def register_user(user:str,user_api_key:str):
    with SqliteDict("./users.sqlite") as sqldict:
        sqldict[user] = user_api_key
        sqldict.commit()

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

