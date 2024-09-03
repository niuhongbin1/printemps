import os
import logging

if os.path.exists("test_file.txt"):
    os.remove('./all.log')

# os.remove('./all.log')
###   logging 设置
logger = logging.getLogger('mylogger')
logger.setLevel(logging.DEBUG)
rf_handler = logging.FileHandler(filename='all.log',encoding='utf-8')
f_handler =   logging.StreamHandler()
f_handler.setLevel(logging.DEBUG)
logger.addHandler(rf_handler)
logger.addHandler(f_handler)
### 