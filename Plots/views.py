import re,base64
from django.contrib.admin.views.decorators import staff_member_required
from . import Mathparse
from .models import Plot
from django.contrib.auth.decorators import login_required
from common.decorators import ajax_required,time_delay_required
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.http import JsonResponse,HttpResponse
from .tasks import createPlotinAdmin


# Create your views here.

def mainV(request):
    return render(request,'calculate.html', {'section':'calculate'})

@time_delay_required
@ajax_required
def calculate(request):
    if request.method == 'POST':
        equation = request.POST.get('equation')
        left = request.POST.get('left')
        right = request.POST.get('right')
        step = request.POST.get('step')
        if(left != '' and right != '' and step != ''):
            data, data_x, ok = Mathparse.mainMathParse(equation,float(left),float(right),float(step))
        else:
            data, data_x, ok = Mathparse.mainMathParse(equation)
    return JsonResponse({'status': ok, 'values':data,'values_x':data_x})


@login_required
@ajax_required
@time_delay_required
def save(request):
    if request.method == "POST":
        image64 = request.POST.get('url')
        function = request.POST.get('function')
        interval = request.POST.get('interval')
        step = request.POST.get('step')
        image64 = re.sub("^data:image/png;base64,","",image64)
        image = base64.b64decode(image64)
        image_name = "plot.png"
        figure = Plot()
        figure.image = ContentFile(image,image_name)
        figure.user = request.user
        figure.function = function
        figure.interval = interval
        figure.step = step
        figure.save()
    return JsonResponse({'status':'ok'})

@login_required
def usersPlots(request):
    user = request.user
    plots = Plot.objects.select_related('user').filter(user = user)
    page = request.GET.get('page')
    paginator = Paginator(plots, 6)
    try:
        plots = paginator.page(page)
    except PageNotAnInteger:
        plots = paginator.page(1)
    except EmptyPage:
        images = paginator.page(paginator.num_pages)
    context = {'q_set_Plots':plots,'section':'MyPlots','page':page}
    return render(request,'myplots.html',context)

@staff_member_required
def add_plots_admin(request):
    if request.method == 'POST':
        equation = request.POST.get('equation')
        left = request.POST.get('left')
        right = request.POST.get('right')
        step = request.POST.get('step')
        user_id = request.user.id
        createPlotinAdmin.delay(equation, left, right, step,user_id) #user)
        return redirect("admin:Plots_plot_changelist")
    else:
        return render(request, 'admin/add_plots/add_plot.html')