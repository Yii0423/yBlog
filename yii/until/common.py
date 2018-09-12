import hashlib
import time
import datetime
import os
from PIL import Image

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


# 制作缩略图
def MakeThumb(path, sizes=(123,)):
    """
    缩略图生成程序 by Neil Chen
    sizes 参数传递要生成的尺寸，可以生成多种尺寸
    """
    base, ext = os.path.splitext(path)
    try:
        im = Image.open(path)
    except IOError:
        return
    mode = im.mode
    if mode not in ('L', 'RGB'):
        if mode == 'RGBA':
            # 透明图片需要加白色底
            alpha = im.split()[3]
            bgmask = alpha.point(lambda x: 255 - x)
            im = im.convert('RGB')
            # paste(color, box, mask)
            im.paste((255, 255, 255), None, bgmask)
        else:
            im = im.convert('RGB')
    width, height = im.size
    if width == height:
        region = im
    else:
        if width > height:
            delta = (width - height) / 2
            box = (delta, 0, delta + height, height)
        else:
            delta = (height - width) / 2
            box = (0, delta, width, delta + width)
        region = im.crop(box)

    for size in sizes:
        filename = base.replace('autouploads/big', 'autouploads/small') + ".jpg"
        thumb = region.resize((size, size), Image.ANTIALIAS)
        thumb.save(filename, quality=100)  # 默认 JPEG 保存质量是 75, 不太清楚。可选值(0~100)
