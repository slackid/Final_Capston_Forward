from flask import Flask, render_template, jsonify, request, json, redirect, Response
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import base64
from flask_bcrypt import Bcrypt
from PIL import Image
from io import BytesIO
import os
from datetime import datetime
import ast
import numpy as np
import cv2
from sitable import Signdatabase
from face import face_function

app = Flask(__name__)
app.config['SECRET_KEY'] = 'BCODE_Flask'
app.config['JWT_SECRET_KEY'] = 'super-secrete'
socketio = SocketIO(app)

jwt = JWTManager(app)
bcrypt = Bcrypt(app)

CORS(app)


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')


@app.route('/static/', methods=['GET', 'POST'])
def home1():
    return render_template('index.html')


# 회원 가입 로직
@app.route('/static/users/register', methods=['POST'])
def register():

    User = {
        'stu_num': request.get_json()['stu_num'],
        'name': request.get_json()['name'],
        'email': request.get_json()['email'],
        'password': bcrypt.generate_password_hash(request.get_json()['password']).decode('utf-8')
    }
    atten(User.get('stu_num'))
    db = Signdatabase()
    msg = db.register(User)
    if msg == True:
        result = {
            "success": True,
            "msg": "등록에 성공하였습니다"
        }
        return result
    else:
        result = {
            "success": False,
            "msg": msg
        }
        return result


# 로그인 로직
@app.route("/static/users/authenticate", methods=['POST'])
def signIn():
    stu_num = request.get_json()['stu_num']
    password = request.get_json()['password']

    db = Signdatabase()
    msg = db.login(stu_num, password)
    if msg == True:
        token = create_access_token(identity={'stu_num': stu_num})
        user = db.getUserbyStu_num(stu_num)
        result = {
            "success": True,
            "msg": "로그인되었습니다",
            "token": token,
            "user": user
        }

        return result

    else:
        result = {
            "success": False,
            "msg": msg

        }
        print(result)
        return result


@app.route("/static/image/decodeImage", methods=['POST'])
def decode():
    user = ast.literal_eval(request.get_json()['user'])
    stu_num = user.get('stu_num')
    name = user.get('name')

    f = open('file.txt', 'w')
    image = request.get_json()['image'].replace('data:image/png;base64,', '')
    f.write(image)
    f.close()
    f = open('file.txt', 'r')
    data = f.read()
    f.closed

    # PIL image
    im = Image.open(BytesIO(base64.b64decode(data)))

    # PIL to cv2
    cv2_image = np.array(im.convert('RGB'))
    cv2_image = cv2_image[:, :, ::-1].copy()

    # import face_function module
    ff = face_function()
    # check face number of picutre
    if ff.check_face_num(cv2_image) == True:

        time_today = str(datetime.now().year) + "." + \
            str(datetime.now().month) + "." + str(datetime.now().day)
        imagedir = 'students/' + str(stu_num) + \
            '_' + name + '/' + time_today + '.jpg'
        if (os.path.isdir('students/' + str(stu_num) + '_' + name)):
            pass
        else:
            os.mkdir('students/' + str(stu_num) + '_' + name)
        # save face as csv
        check = ff.registerimage(cv2_image, stu_num, name)

        # 얼굴 인식 확인 및 이미지 저장
        # save face as csv
        check = ff.registerimage(cv2_image, stu_num, name)

        time_today = str(datetime.now().year) + "." + \
            str(datetime.now().month) + "." + str(datetime.now().day)
        imagedir = 'students/' + str(stu_num) + \
            '_' + name + '/' + time_today + '.jpg'

        # 얼굴 인식 확인 및 이미지 저장
        if check == True:
            im.save(imagedir, 'png')
            result = {
                "success": True,
                "msg": "얼굴 데이터셋 생성 성공"
            }
            return result

        elif check == False:
            result = {
                "success": False,
                "msg": "얼굴 인식이 실패하였습니다"
            }
            return result

    else:
        result = {
            "success": False,
            "msg": "얼굴이 인식되지 않았거나 두개 이상입니다"
        }
        return result


@app.route("/static/image/encode/send", methods=["POST", "GET"])
def imgSend():
    if request.method == "POST":
        name = request.get_json()[0]['name']
        stu_num = request.get_json()[0]['stu_num']
        date = request.get_json()[0]['date']
        try:
            result = {
                "msg": imgencode(name, stu_num, date).decode('utf-8')
            }
            return result
        except:
            result = {
                "msg": None
            }
            return result


def imgencode(name, stu_num, date):
    with open("./students/{}_{}/{}.jpg".format(stu_num, name, date), "rb") as img_file:
        my_string = base64.b64encode(img_file.read())

    return my_string


# 로그아웃 로직
@app.route('/logout')
def logout():
    custom_resp = Response("COOKIE 제거")
    custom_resp.set_cookie('USERID', expires=0)
    return custom_resp


# 쿠키 값 확인 로직
@app.route("/loginstatus")
def cookie_status():
    tempstr = request.cookies.get('stu_num', '빈문자열')
    tempstr = tempstr.encode("UTF-8")

    return (base64.b64decode(tempstr)).decode('UTF-8')


def atten(stunum):
    db = Signdatabase()
    a, b, c, f = map(int, '2020,08,25,11'.split(','))
    import datetime
    for i in range(16):
        d = datetime.datetime(a, b, c, f)+datetime.timedelta(weeks=i)
        attend = {
            'stu_num': stunum,
            'week': i+1,
            'atten_date': d.strftime('%Y-%m-%d %H'),
            'atten': "None"
        }

        db.attendInsert(attend)


# 과목 조회
@app.route("/static/subject/info", methods=["POST"])
def subject_info():

    db = Signdatabase()
    temp = db.get_subjectInfo(request.get_json()['stu_num'])
    result = {
        'msg': temp
    }
    return result


def subject_index():
    a, b, c = map(int, input().split(','))
    for i in range(16):
        d = datetime.datetime(a, b, c)+datetime.timedelta(weeks=i)
        print(d.strftime('%Y-%m-%d'))


@app.route("/static/atten/attend", methods=["POST"])
def attendance_check():
    data = request.get_json()[0]
    stu_num = data['stu_num']
    week = data['week']
    db = Signdatabase()
    # attend_update 로직 필요
    db.update_atten(stu_num, week, atten_update(True))
    return "UPDATE ON "


def atten_update(face_data):
    import datetime
    if face_data == True:
        db = Signdatabase()
        bc = db.temp()
        bc = bc['atten_date']
        cutline = datetime.datetime.now()-bc
        print(cutline)
        if cutline < datetime.timedelta(hours=2):
            return "출석"
        elif cutline > datetime.timedelta(hours=2):
            return "지각"
    elif face_data == False:
        return "결석"


socketio.run(app, port=9999, debug=True)
