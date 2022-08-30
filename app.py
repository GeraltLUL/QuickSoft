from bson import json_util
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask import render_template, make_response, redirect, url_for, flash, session, Flask, request
from flask_cors import CORS
from pymongo import MongoClient
from mongodb import *
from validation import input_form_correct
import pdfkit
from werkzeug.utils import secure_filename
import os
import re

# Flask config
app = Flask(__name__)
app.config['SECRET_KEY'] = '12s32gds32f1523das3df'
app.config['JSON_AS_ASCII'] = False
app.config['SECURITY_UNAUTHORIZED_VIEW'] = '/login'
app.config['UPLOAD_IMAGE_FOLDER'] = './static/assets/img/usersAvatars'
app.config.from_object(__name__)
CORS(app)

client = MongoClient('localhost', 27017)
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
            print(request.get_json())
            data = request.get_json()
            cur_user = find_user_by_email(str(data['email']))

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
@app.route('/upload_avatar', methods=['GET', 'POST'])
@login_required
def upload_avatar():
    # cur_user_id = session['id']
    cur_user_id = current_user.id
    avatar = request.files['avatar']
    avatar_name = avatar.filename

    if request.method == 'POST':
        if avatar is not None:
            if avatar_name[-3:] in ["jpg", "png"]:
                file_name = f"{avatar_name[:-4]}-id-{uuid.uuid4()}.{avatar_name[-3:]}"
                avatar.save(os.path.join(app.config['UPLOAD_IMAGE_FOLDER'], file_name))
                update_record('id', cur_user_id, 'avatar', file_name)

    return redirect(url_for('profile'))


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
            len_of_user = 3

            for i in range(len(req_data)//len_of_user):
                x = request.form.get(f'x[{i}]').split(',')
                y = request.form.get(f'y[{i}]').split(',')
                user_id = request.form.get(f'id[{i}]')

                user_data = {'x': [], 'y': []}

                for j in range(len(x)):
                    user_data['x'].append(int(x[j]))
                    user_data['y'].append(int(y[j]))
                print(user_data)
                update_and_push('id', user_id, 'gameSessions', user_data)

            return '200'
        except Exception as e:
            print(e)


@app.route('/get_game_sessions', methods=['GET'])
@login_required
def get_game_sessions():
    try:
        return {'userSessionsData': current_user.gameSessions}
    except Exception as e:
        print(e)


if __name__ == '__main__':
    app.run(debug=False)
