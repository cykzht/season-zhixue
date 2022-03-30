# Season-zhixue

### 介绍
四季学——退学网，可以绕过某学网的限制，获取到自己真实的成绩。

正如它的名字一样，这是一个会变换四季的程序，每次启动的时候都会重新选择一个季节作为主题季节。



### 安装教程
#### 环境配置

```python
pip3 install flask
pip3 install zhixuewang
pip3 install flask_limiter
```


### 使用说明

1、安装好所需的库之后运行Python程序（开箱即用）。

2、访问[http://127.0.0.1:5000/](http://127.0.0.1:5000)访问四季学网站。

3、输入某学网的账号和密码即可查询最新一次的考试成绩。


### TODO

- [x] 记住密码
（貌似不起作用，在Javascript里，使用cookie）
- [ ] 排名查询
（找不到接口）
- [ ] 历史成绩查询
（没什么大用，主要是接口调用太复杂，咕了）


### 修改建议

1. 如果要使用cookie或者session请先配置一下密钥。

```python
app.config["SECRET_KEY"] = 'abc'  # 配置密钥
```
2. 如需控制网站访问量可以设置Limiter。

```python
limiter = Limiter(  # 限制访问量
    app,
    key_func=get_remote_address,  # 根据访问者的IP记录访问次数
    default_limits=["200 per day", "20 per minute"]  # 默认限制，一分钟最多访问20次
)
```
2. 如果你的网站使用了Nginx代理，请为Limiter加入以下代码。
```python
def limit_key_func():
    return str(request.headers.get("X-Forwarded-For", '127.0.0.1'))
limiter = Limiter(  # 限制访问量
    app,
    key_func=limit_key_func,  # 根据访问者的IP记录访问次数
    default_limits=["200 per day", "20 per minute"]  # 默认限制，一分钟最多访问20次
)
```
3. 错误页面在[error.html](templates/error.html)里。



### 参与贡献

本项目的诞生离不开[zhixuewang](https://github.com/anwenhu/zhixuewang-python)、[layui](https://gitee.com/sentsin/layui)、[Flask](https://github.com/pallets/flask)。

