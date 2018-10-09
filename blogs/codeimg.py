from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import random
# 获取rgb随机的颜色参数
def get_random_color():
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
# 获取验证码图片函数
def get_valid_code_img(request):
    img = Image.new("RGB", (170, 30), color=get_random_color())
    draw = ImageDraw.Draw(img)
    kumo_font = ImageFont.truetype("arial.ttf", size=26)
    valid_code_str = ""
    for i in range(4):
        random_num = str(random.randint(0, 9))
        random_low_alpha = chr(random.randint(95, 122))
        random_upper_alpha = chr(random.randint(65, 90))
        random_char = random.choice([random_num, random_low_alpha, random_upper_alpha])
        draw.text((i * 30 + 30, 0), random_char, get_random_color(), font=kumo_font)
        # 保存验证码字符串
        valid_code_str += random_char
    # 噪点噪线
    width=170
    height=30
    # for i in range(3):
    #     x1=random.randint(0,width)
    #     x2=random.randint(0,width)
    #     y1=random.randint(0,height)
    #     y2=random.randint(0,height)
    #     draw.line((x1,y1,x2,y2),fill=get_random_color())
    for i in range(50):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=get_random_color())
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.arc((x, y, x + 4, y + 4), 0, 90, fill=get_random_color())
    request.session["valid_code_str"] = valid_code_str
    request.session['count'] = 0
    f = BytesIO()
    img.save(f, "png")
    data = f.getvalue()
    return data