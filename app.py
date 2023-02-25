from flask import *
import random
from zhixuewang import login_student
import base64
import requests

app = Flask(__name__, static_url_path='')
app.config["SECRET_KEY"] = 'abc'  # 配置密钥


# 错误返回
@app.errorhandler(404)
@app.errorhandler(500)
@app.errorhandler(429)
def error(e):
    if (e.code == 404):
        return render_template("error.html", msg='404错误，页面不存在。', code=404)
    elif (e.code == 500):
        return render_template("error.html", msg='500服务器内部错误。', code=500)
    elif (e.code == 429):
        return render_template("error.html", msg='429访问过于频繁，请稍后再试。', code=429)
    else:
        return render_template("error.html", msg='500服务器内部错误。', code=500)


def get_season():
    '''
    随机选取季节
    slog: 季节名
    pic: 背景图片
    color: 主题颜色
    '''
    ran = random.randint(1, 4)
    if (ran == 1):
        slog = '退学网——秋'
        color = '#e5bc00'
        pic = 'images/web_login_bg1.webp'
    elif (ran == 2):
        slog = '退学网——夏'
        color = '#50e45c'
        pic = 'images/web_login_bg2.webp'
    elif (ran == 3):
        slog = '退学网——春'
        color = '#f1beea'
        pic = 'images/web_login_bg3.webp'
    elif (ran == 4):
        slog = '退学网——冬'
        color = '#27A9E3'
        pic = 'images/web_login_bg4.webp'
    return slog, pic, color


@app.route('/', methods=['GET', 'POST'])
def index():
    season = get_season()
    session['season'] = season
    if (request.method == 'POST'):
        username = request.form.get("username")
        password = request.form.get("password")
        session['username'] = username
        session['password'] = password
        return redirect(url_for('login'))
    if (session.get('username')):
        return redirect(url_for('login'))
    else:
        return render_template('index.html', season=season)


@app.route('/mark', methods=['GET', 'POST'])
def login():
    season = session.get('season')
    if (not season):
        season = get_season()
    # 处理登录请求
    if (not session.get('username')):
        return redirect(url_for('index'))
    else:
        username = session.get('username')
        password = session.get('password')
        exam = request.args.get('exam')
        try:
            zxw = login_student(username, password)
            exams = zxw.get_exams()
        except Exception as e:
            session.clear()
            return render_template("index.html", season=season, message=e)
        if len(exams) != 0:
            data = []
            examlist = []
            for i in exams:
                data.append(i.id)
                examlist.append((i.id, i.name))
            try:
                pic = requests.get(zxw.avatar).content
                avatar = base64.b64encode(pic)
                avatar = 'data:image/png;base64,'+str(avatar, 'utf-8')
            except:
                avatar = 'images/avatar_default_student_200_m_3.png'
            if (exam):
                if (exam in data):
                    try:
                        a = zxw.get_self_mark(exam)
                    except Exception as e:
                        return render_template("examlist.html", data=examlist, season=season, avatar=avatar, message="本场考试未扫描")
                    msg = a.person.name+'-'+a.exam.name
                    data = []
                    for i in a:
                        if (i.class_rank):
                            data.append(
                                (i.subject.name, i.score, i.class_rank))
                        else:
                            data.append((i.subject.name, i.score))
                    return render_template("zhixue.html", data=data, season=season, title=msg, avatar=avatar)
                else:
                    return render_template("examlist.html", data=examlist, season=season, avatar=avatar, message="该考试不可查询")
            else:
                return render_template("examlist.html", data=examlist, season=season, avatar=avatar)
        else:
            return render_template("index.html", season=season, message='未检测到考试')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=6082, debug=True)
