from os import environ
import firebase_admin
from firebase_admin import db

from encrypt import encrypt_credentials, decrypt_credentials

cred_obj2 = firebase_admin.credentials.Certificate('api_database.json')
app2 = firebase_admin.initialize_app(cred_obj2, {'databaseURL': 'https://toornamnet-bot-default-rtdb.firebaseio.com/'},
                                     name='app2')
ref2 = db.reference('/', app2)


def register(username, password):
    if (sign_in(username, password, 1)): return False
    try:
        index = str(len(ref2.get()))
    except TypeError:
        index = '0'
    ref2.child(index).update(
        {'username': encrypt_credentials(username), 'password': encrypt_credentials(password), 'subscription_type': 0})
    return True


def sign_in(username, password, check_for_sub=0):
    try:
        for x in ref2.get():
            if (decrypt_credentials(x.get('username')) == username):
                if (decrypt_credentials(x.get('password')) == password):
                    if (x.get('subscription_type') or check_for_sub):
                        return True
    except AttributeError as e:
        print(e)
    return False
