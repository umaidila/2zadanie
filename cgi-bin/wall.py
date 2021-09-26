#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cgi
import html
import http.cookies
import os

from _wall import Wall
wall = Wall()

cookie = http.cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
session = cookie.get("session")
if session is not None:
    session = session.value
user = wall.find_cookie(session)  # Ищем пользователя по переданной куке

message = ""

form = cgi.FieldStorage()
action = form.getfirst("action", "")

if action == "publish":
    text = form.getfirst("text", "")
    text = html.escape(text)

    if text and user is not None:
        wall.publish(user, text)
elif action == "login":
    login = form.getfirst("login", "")
    login = html.escape(login)
    password = form.getfirst("password", "")
    password = html.escape(password)
    if wall.find(login, password):
        cookie = wall.set_cookie(login)
        print('Set-cookie: session={}'.format(cookie))
    elif wall.find(login):
        message = "<font color='red'>Неверный пароль</font>"
    else:
        wall.register(login, password)
        cookie = wall.set_cookie(login)
        print('Set-cookie: session={}'.format(cookie))
        message = "<font color='green'>Успешная регистрация, для входа введите данные ещё раз</font>"
elif action == "clear":
    wall.clear()
elif action == "logout":
    user = None



pattern = '''
<!DOCTYPE HTML>
<html>
<head>
<meta charset="utf-8">
<title>Стена</title>

</head>
<body>
    Форма логина и регистрации. При вводе несуществующего имени зарегистрируется новый пользователь.
    <form action="/cgi-bin/wall.py">
        Логин: <input type="text" name="login">
        Пароль: <input type="password" name="password">
        <input type="hidden" name="action" value="login">
        <input type="submit"> {message1}
    </form>
    
    <form action="/cgi-bin/wall.py">
    <input type="hidden" name="action" value="logout">
    Ваш логин: {user1}
    </form>
    
    {posts}

    {publish}
    
    
</body>
</html>
'''

if user is not None and user != "":
    pub = '''
    <form action="/cgi-bin/wall.py">
        <textarea name="text" id = "textarea"></textarea>
        <input type="hidden" name="action" value="publish">
        <input type="submit">
        <br/>
        <input type="button" value = "😁" onclick = "s1()">
        <input type="button" value = "😃" onclick = "s2()">
        <input type="button" value = "😇" onclick = "s3()">
        <input type="button" value = "😉" onclick = "s4()">
        <input type="button" value = "😘" onclick = "s5()">
        <input type="button" value = "😝" onclick = "s6()">
        </form>
        <br/>
        <br/>
        <form action="/cgi-bin/wall.py">
        <input type="hidden" name="action" value="clear">
        Стереть историю - 
        <input type = "submit">
        </form> 
    <script>
    
    function s1(){
        document.getElementById('textarea').value = document.getElementById('textarea').value + "😁" ;
        }
    function s2(){
        document.getElementById('textarea').value = document.getElementById('textarea').value + "😃" ;
        }
        function s3(){
        document.getElementById('textarea').value = document.getElementById('textarea').value + "😇" ;
        }
        function s4(){
        document.getElementById('textarea').value = document.getElementById('textarea').value + "😉" ;
        }
        function s5(){
        document.getElementById('textarea').value = document.getElementById('textarea').value + "😘" ;
        }
        function s6(){
        document.getElementById('textarea').value = document.getElementById('textarea').value + "😝" ;
        }
        </script>
    '''
else:
    pub = ''

print('Content-type: text/html\n')
if user is None or user == "":
    user = "<font color='red'> вы не вошли в аккаунт</font>"
else:
    user = user + " <input type='submit' value='Выйти'> "

print(pattern.format(posts=wall.html_list(), publish=pub,user1 = user, message1 = message))