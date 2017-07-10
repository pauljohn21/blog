#! coding:utf-8

def user_verify(form):
    _user = {}
    if isinstance(form,dict):
        for key,value in form.items():
            if key and value:
                _user.update({key:value})
    return _user