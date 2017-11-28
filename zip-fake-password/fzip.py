#-*-coding:utf-8-*-

"""
用于处理zip的伪加密
CTF常见的ZIP玩法之一，修改加密标记位，让解压软件误认为加密。
参考 http://blog.csdn.net/ETF6996/article/details/51946250
"""
__author__ = 'hellotimo'

import getopt
import sys
import os

def zip_header(f, data, crypt=True):
    i = data.find('\x50\x4B\x03\x04')
    if i == -1: return
    f.seek(i + 6, 0)
    f.write('\x01' if crypt else '\x00')
    
def file_header(f, data, crypt=True):
    j = -1
    i = 0
    while True:
        j = data[:j].rfind('\x50\x4B\x01\x02')
        if (j == -1): break
        f.seek(j + 8, 0)
        f.write('\x01' if crypt else '\x00')
        i+=1
    print u'Found and modified %s flag(s)' % i

def main(filename, crypt):
    f = open(filename,'rb+')
    data = f.read()
    zip_header(f, data, crypt)
    file_header(f, data, crypt)
    f.close()

def usage():
    print u'''用法：
生成伪加密   fzip.py -e file.zip
去除伪加密   fzip.py -d file.zip
'''

if __name__=='__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:],'e:d:')
        for o,v in opts:
            if o == '-e':
                main(v, True)
                break
            elif o == '-d':
                main(v, False)
                break
                
        else:
            usage()
        #print (opts)
        #print (args)
        
    except getopt.GetoptError:
        usage()
        sys.exit()
        