from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrapper_func(request,*args, **kwargs):
        if request.user.is_authenticated:
            return redirect('blog:post_list')
        else:    
            return view_func(request,*args, **kwargs)
    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_fuc(request,*args, **kwargs):
           
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request,*args, **kwargs)
            else:
                return HttpResponse("You are not allowd to view the page")
        return wrapper_fuc
    return decorator

def admin_only(view_func):
        def wrapper_fuc(request,*args, **kwargs):
           
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group == 'Admin':
                return view_func(request,*args, **kwargs)
            else:
                return HttpResponse("You are not allowd to view the page")
        return wrapper_fuc