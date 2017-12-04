import os
import random
import string
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# 字体的位置，不同版本的系统会有不同
font_path = os.path.dirname(__file__) + '/../static/admin/font/Arial.ttf'
# 生成几位数的验证码
number = 4
# 生成验证码图片的高度和宽度
size = (100, 38)
# 背景颜色，默认为白色
bgcolor = (255, 255, 255)
# 字体颜色，默认为蓝色
fontcolor = (0, 0, 255)
# 干扰线颜色。默认为红色
linecolor = (255, 0, 0)
# 是否要加入干扰线
draw_line = True
# 加入干扰线条数的上下限
line_number = (1, 5)


# 用来随机生成一个字符串
def gene_text():
    source = list(string.ascii_letters)
    for index in range(0, 10):
        source.append(str(index))
    return ''.join(random.sample(source, number))  # number是生成验证码的位数


# 用来绘制干扰线
def gene_line(draw, width, height):
    begin = (random.randint(0, width), random.randint(0, height))
    end = (random.randint(0, width), random.randint(0, height))
    draw.line([begin, end], fill=linecolor)


# 生成验证码
def gene_code(request):
    width, height = size  # 宽和高
    image = Image.new('RGBA', (width, height), bgcolor)  # 创建图片
    font = ImageFont.truetype(font_path, 30)  # 验证码的字体
    draw = ImageDraw.Draw(image)  # 创建画笔
    text = gene_text().lower()  # 生成字符串
    request.session['code'] = text
    font_width, font_height = font.getsize(text)
    draw.text(((width - font_width) / number, (height - font_height) / number), text,
              font=font, fill=fontcolor)  # 填充字符串
    if draw_line:
        gene_line(draw, width, height)
    # image = image.transform((width + 20, height + 10), Image.AFFINE, (1, -0.3, 0, -0.1, 1, 0), Image.BILINEAR)  # 创建扭曲
    image = image.filter(ImageFilter.EDGE_ENHANCE_MORE)  # 滤镜，边界加强
    image.save(os.path.dirname(__file__) + '/../static/admin/images/code.jpg', 'png')  # 保存验证码图片


if __name__ == "__main__":
    gene_code()
