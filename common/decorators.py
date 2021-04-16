from django.http import HttpResponseBadRequest,JsonResponse,HttpResponse
import time


def ajax_required(f):
    def wrap(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest()
        return f(request, *args, **kwargs)
    wrap.__doc__=f.__doc__
    wrap.__name__=f.__name__
    return wrap


def time_delay_required(f):
    then = 0
    def wrap(request,*args,**kwargs):
        ntime = time.time()
        nonlocal then
        if(ntime-then>=0):
            then = ntime + 5
            return f(request,*args,**kwargs)
        return JsonResponse({'status':'Time delay'})
    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap




