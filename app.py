from flask import *
import random
from zhixuewang import login_student
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
app = Flask(__name__, static_url_path='')
app.config["SECRET_KEY"] = 'abc'  # 配置密钥

limiter = Limiter(  # 限制访问量
    app,
    key_func=get_remote_address,  # 根据访问者的IP记录访问次数
    default_limits=["200 per day", "20 per minute"]  # 默认限制，一分钟最多访问20次
)

# 错误返回


@app.errorhandler(404)
def miss(e):
    return render_template("error.html", msg='404 Not Found.')


@app.errorhandler(500)
def error(e):
    return render_template("error.html", msg='500 IIS Error.')


@app.errorhandler(429)
def error(e):
    return render_template("error.html", msg='429 Too Frequently.')


# 主界面
@app.route('/', methods=['GET', 'POST'])
@limiter.exempt
def index():
    # 随机选取季节
    ran = random.randint(1, 4)
    if(ran == 1):
        slog = '退学网——秋'
        color = '#e5bc00'
        pic = 'images/web_login_bg1.jpg'
    elif(ran == 2):
        slog = '退学网——夏'
        color = '#50e45c'
        pic = 'images/web_login_bg2.jpg'
    elif(ran == 3):
        slog = '退学网——春'
        color = '#f1beea'
        pic = 'images/web_login_bg3.jpg'
    elif(ran == 4):
        slog = '退学网——冬'
        color = '#27A9E3'
        pic = 'images/web_login_bg4.jpg'
    # 处理登录请求
    if(request.method == 'POST' and request.values.get("username")):
        data = []
        c = []
        d = []
        username = request.values.get("username")
        password = request.values.get("password")
        exams = 0
        try:
            zxw = login_student(username, password)
            exams = zxw.get_exams()
        except:
            return render_template("index.html", slog=slog, pic=pic, color=color, msg='账号或密码错误')
        if len(exams) != 0:
            a = zxw.get_self_mark()
            a = str(a)
            a = a.split("\n")
            b = a[0]
            del a[0]
            for i in a:
                if("分数" in i):
                    c.append(i)
                else:
                    d.append(i)
            for i in range(len(c)):
                data.append((d[i].replace(':', ''), c[i].replace('分数: ', '')))
            return render_template("zhixue.html", data=data, title=b, pic=pic, color=color)
        else:
            return render_template("index.html", slog=slog, pic=pic, color=color, msg='未检测到考试')
    return render_template('index.html', slog=slog, pic=pic, color=color)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
