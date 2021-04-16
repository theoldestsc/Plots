import io
from celery import task
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.mail import send_mail
from .models import Plot
from . import Mathparse
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot
from PIL import Image, ImageDraw, ImageFont

@task
def createPlotinAdmin(equation,left,right,step,user_id):
    if (left != '' and right != '' and step != ''):
        data, data_x, ok = Mathparse.mainMathParse(equation, float(left), float(right), float(step))
    else:
        data, data_x, ok = Mathparse.mainMathParse(equation)
    if(ok == ""):
        fig, ax = pyplot.subplots()  # Получаю 2 области, области внутри осей и за осями
        ax.set(facecolor='#191930')
        ax.tick_params(axis='both', which='minor', labelcolor='#00CED1')
        pyplot.plot(data,data_x, color='#00CED1')
        pyplot.grid(color='w', linewidth=0.5)
        buf = io.BytesIO()
        fig.savefig(buf, format="png", facecolor='#38486F')
        figure = Plot()
        image_name = "plot.png"
        figure.image = ContentFile(buf.getvalue(),image_name)
        figure.user = User.objects.get(id = user_id)
        figure.function = equation
        figure.interval = step
        figure.step = step
        figure.save()
    else:
        W, H = (300, 120)
        img = Image.new("RGB", (W, H), (255, 255, 255))
        idraw = ImageDraw.Draw(img)
        text = "High Tatras"
        font = ImageFont.truetype("arial.ttf", size=18)
        w, h = idraw.textsize(text, font=font)
        idraw.text(((W - w) / 2, (H - h) / 2), text, font=font, fill=(0, 0, 0))

        buf = io.BytesIO()
        img.savefig(buf, format="png", facecolor='#38486F')
        figure = Plot()
        image_name = "plot.png"
        figure.image = ContentFile(buf.getvalue(), image_name)
        figure.user = User.objects.get(id=user_id)
        figure.function = equation
        figure.interval = step
        figure.step = step
        figure.save()
    return 1

#celery -A <module> worker -l info -P eventlet