import hashlib
import os

def md5(string):
    m = hashlib.md5()
    m.update(string)
    return m.hexdigest()

username = 'timo@god.home'
_username = raw_input("Input your username:(%s)"% username)
if _username: username = _username

keycode = md5("new Sprite()" + md5(username) + "_laan_soft_776") + "15"
print '''=======================================
username:
%s
keycode:
%s
=======================================
''' % (username, keycode)
    
os.system('pause')