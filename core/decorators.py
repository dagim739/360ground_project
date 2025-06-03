from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse



def hx_request_only(view_func):
    def wrapper(request):
        if request.headers.get('HX-Request') == 'true':
            return view_func(request)
        else:
            return HttpResponse('BadRequest')
    return wrapper





def require_login(view_func):
    def wrapper(request):
        if 'status' in request.session:
            if request.session['status'] == 'logged_in':
                return view_func(request)
            else:
                return HttpResponseRedirect(reverse('log_in'))
        else:
            return HttpResponseRedirect(reverse('log_in'))
    return wrapper