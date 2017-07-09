import json




def user_to_dict(users):
    _users = {"users":[]}
    if len(users) > 0:
        for user in users:
            _u = dict(user)
            _u['last_login_time'] = _u['last_login_time'].strftime('%Y-%m-%d %H:%M:%S')
            _users['users'].append(_u)
        return _users

def posts_to_dict(posts):
    _posts = {"posts":[]}
    if len(posts) > 0:
        for post in posts:
            _p = dict(post)
            _p['create_time'] = _p['create_time'].strftime("%Y-%m-%d %H:%M:%S")
            _posts['posts'].append(_p)
        return _posts





