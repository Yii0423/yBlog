import hashlib
import time
import datetime

# UTC时间转本地时间(+8:00)
from Blog.settings import ENCRYPT_KEY


def utc2local(utc_st, type=1):
    now_stamp = time.time()
    local_time = datetime.datetime.fromtimestamp(now_stamp)
    utc_time = datetime.datetime.utcfromtimestamp(now_stamp)
    offset = local_time - utc_time
    local_st = datetime.datetime.strptime(utc_st, "%Y-%m-%dT%H:%M:%S.%fZ") + offset
    if type == 0:
        return str(local_st)
    if type == 1:
        return str(local_st)[0:19]
    if type == 2:
        return str(local_st)[0:10]
    if type == 3:
        return str(local_st)[11:19]


# 加密
def encrypt(content):
    hash = hashlib.md5(ENCRYPT_KEY.encode('utf-8'))
    hash.update(content.encode('utf-8'))
    return hash.hexdigest()
