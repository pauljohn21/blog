#! coding:utf-8

def user_verify(form):
    _user = {}
    if isinstance(form,dict):
        for key,value in form.items():
            if key and value:
                if isinstance(value,tuple):
                    pass
    return _user