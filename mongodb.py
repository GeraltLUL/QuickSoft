from app import collection
from flask_login import UserMixin
import uuid
from datetime import datetime


class User(UserMixin):
    id = ''
    name = ''
    email = ''
    password = ''
    registerDate = ''
    avatar = ''
    gameSessions = []

    def __init__(self, id, name, email, password, registerDate, avatar, gameSessions):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.registerDate = registerDate
        self.avatar = avatar
        self.gameSessions = gameSessions

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False


def create_record(data):
    date_now = datetime.now()
    now_month = date_now.month
    now_day = date_now.day

    if now_month <= 10:
        now_month = f"0{now_month}"

    if now_day <= 10:
        now_day = f"0{now_day}"

    collection.insert_one({
        'id': str(uuid.uuid4()),
        'name': data['name'],
        'email': data['email'],
        'password': data['password'],
        'registerDate': f"{now_day}.{now_month}.{date_now.year}",
        'avatar': 'user_tmp_example.png',
        'gameSessions': []
    })


def find_user_by_id(user_id):
    cur_user = collection.find_one({'id': user_id})
    if cur_user is not None:
        return User(id=cur_user['id'],
                    name=cur_user['name'],
                    email=cur_user['email'],
                    password=cur_user['password'],
                    registerDate=cur_user['registerDate'],
                    avatar=cur_user['avatar'],
                    gameSessions=cur_user['gameSessions'])
    else:
        return None


def find_user_by_email(value):
    cur_user = collection.find_one({'email': value})
    if cur_user is not None:
        return User(id=cur_user['id'],
                    name=cur_user['name'],
                    email=cur_user['email'],
                    password=cur_user['password'],
                    registerDate=cur_user['registerDate'],
                    avatar=cur_user['avatar'],
                    gameSessions=cur_user['gameSessions'])
    else:
        return None


def delete_record_by_id(value):
    collection.delete_one({
        'id': value
    })


def update_record(findKey, findValue, key, value):
    collection.find_one_and_update({findKey: findValue},
                                   {'$set': {key: value}})


def update_and_push(findKey, findValue, key, value):
    collection.find_one_and_update({findKey: findValue},
                                   {'$push': {key: value}})
