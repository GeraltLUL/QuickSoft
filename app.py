from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask import render_template, redirect, url_for, session, Flask, request
from flask_cors import CORS
from pymongo import MongoClient
from validation import input_form_correct
import os
from flask_login import UserMixin
import uuid
# import yadisk
from datetime import datetime

# Flask config
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_KEY')
app.config['JSON_AS_ASCII'] = False
app.config['SECURITY_UNAUTHORIZED_VIEW'] = '/login'
app.config['UPLOAD_IMAGE_FOLDER'] = './static/assets/img/usersAvatars'
app.config.from_object(__name__)
CORS(app)

client = MongoClient(os.getenv('MONGODB_URI'))
db = client['QuickSoft']
collection = db['users']

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access the site'
login_manager.login_message_category = 'success'


# @app.errorhandler(404)
# @app.errorhandler(401)
# def page_not_found(error):
#     return render_template('notfound.html')


@login_manager.user_loader
def load_user(user_id):
    return find_user_by_id(user_id)


@app.after_request
def apply_caching(response):
    response.headers['X-Frame-Options'] = 'ALLOW'
    return response


# Main page
@app.route('/')
def index():
    username = None
    if session.get('username'):
        username = session.get('username')

    return render_template('index.html', username=username)


# Profile Page
@app.route('/profile')
@login_required
def profile():
    username = session.get('username')
    return render_template('profile.html',
                           username=username,
                           registerDate=current_user.registerDate,
                           avatar=current_user.avatar)


# Login
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        try:
            data = request.get_json()
            cur_user = find_user_by_email(str(data['email']))
            print(data)

            if cur_user is not None and cur_user.password == str(data['password']):
                session['username'] = cur_user.name
                session['id'] = cur_user.id
                login_user(cur_user)
                return {
                    'msg': f'Добро пожаловать, <strong>{cur_user.name}</strong>!',
                    'category': 'Success',
                    'name': cur_user.name
                }
            else:
                return {
                    'msg': 'Неверный пароль или email!',
                    'category': 'Error'
                }
        except Exception as e:
            print(e)
            return {
                'msg': e,
                'category': 'Error'
            }
    # return {
    #     'msg': 'Unknown Error!',
    #     'category': 'Error'
    # }


# Login
@app.route('/loginTest', methods=['POST', 'GET'])
def loginTest():
    if request.method == 'POST':
        try:
            req_data = request.form.to_dict()
            print(req_data)

            cur_user = find_user_by_email(request.form.get('email'))

            if cur_user is not None and cur_user.password == str(request.form.get('password')):
                session['username'] = cur_user.name
                session['id'] = cur_user.id
                login_user(cur_user)
                return {
                    'msg': f'Добро пожаловать, <strong>{cur_user.name}</strong>!',
                    'category': 'Success',
                    'name': cur_user.name,
                    'id': cur_user.id
                }
            else:
                return {
                    'msg': 'Неверный пароль или email!',
                    'category': 'Error'
                }
        except Exception as e:
            print(e)
            return {
                'msg': e,
                'category': 'Error'
            }
    # return {
    #     'msg': 'Unknown Error!',
    #     'category': 'Error'
    # }


# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            data = request.get_json()

            if input_form_correct(data):
                cur_user = find_user_by_email(str(data['email']))

                if cur_user is None:
                    create_record(data)
                    cur_user = find_user_by_email(str(data['email']))
                    session['username'] = data['name']
                    session['id'] = cur_user.id
                    login_user(cur_user)

                    return {
                        'msg': f'Привет, <strong>{data["name"]}</strong>, вы успешно зарегестрировались и авторизовались!',
                        'category': 'Success',
                        'name': data['name']
                    }
                else:
                    return {
                        'msg': 'Пользователь с таким email уже существует!',
                        'category': 'Error'
                    }
            else:
                return {
                    'msg': 'Поля заполнены некорректно!',
                    'category': 'Error'
                }
        except Exception as e:
            print(e)
            return {
                'msg': e,
                'category': 'Error'
            }

    # return {
    #     'msg': 'Unknown error!',
    #     'category': 'Error'
    # }


# Avatar uploading
# @app.route('/upload_avatar', methods=['POST'])
# @login_required
# def upload_avatar():
#     avatar = request.files['avatar']
#     avatar_name = avatar.filename
#
#     if request.method == 'POST':
#         if avatar is not None:
#             if avatar_name[-3:] in ["jpg", "png"]:
#                 y = yadisk.YaDisk(token=os.getenv('YANDEX_API_KEY'))
#                 print(y)
#                 print(avatar)
#                 print(avatar_name)
#                 file_name = f"{avatar_name[:-4]}-id-{uuid.uuid4()}.{avatar_name[-3:]}"
#                 print(file_name)
#                 y.upload(f'{avatar}', f'/QuickSoft/UsersAvatars/{file_name}')
#                 #avatar.save(os.path.join(app.config['UPLOAD_IMAGE_FOLDER'], file_name))
#                 update_record('id', current_user.id, 'avatar', file_name)
#
#     return redirect(url_for('profile'))


# Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('username', default=None)
    session.pop('id', default=None)
    # flash("You logged out of the profile", 'success')
    return redirect(url_for('index'))


@app.route('/save_game_session', methods=['POST', 'GET'])
def save_game_session():
    if request.method == 'POST':
        try:
            req_data = request.form.to_dict()
            print(req_data)

            x = request.form.get('x').split(';')
            y = request.form.get('y').split(';')
            user_id = request.form.get('id')

            user_data = {'x': [], 'y': []}

            for j in range(len(x)):
                user_data['x'].append(float(x[j].replace(',', '.')))
                user_data['y'].append(float(y[j].replace(',', '.')))

            user_data['sessionId'] = str(uuid.uuid4())

            update_and_push('id', user_id, 'gameSessions', user_data)

            return '200'
        except Exception as e:
            print(e)
            return '500'


@app.route('/get_game_sessions', methods=['GET'])
@login_required
def get_game_sessions():
    try:
        return {'userSessionsData': current_user.gameSessions}
    except Exception as e:
        print(e)


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


if __name__ == '__main__':
    app.run(debug=False)
