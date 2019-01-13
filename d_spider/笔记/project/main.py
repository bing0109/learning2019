# from .selenium_jd_meishi_0111 import jd_meishi
# from .mezitu_0110 import meizitu
# from .selenium_jd_meishi_0111.test1 import main as test1
# from .mezitu_0110 import test2

import time

import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)


str1 = 'sudo python3 meizitu_0110/meizitu.py'
str2 = 'sudo python3 selenium_jd_meishi_0111/jd_meishi.py'
# str2 = 'sudo python3 selenium_jd_meishi_0111/test1.py'
# str1 = 'sudo python3 meizitu_0110/test2.py'

p1 = os.system(str1)
print('--p1--')

time.sleep(3)

p2 = os.system(str2)
print('--p2--')
