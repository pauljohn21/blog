import json




def user_to_dict(users):
    _users = {"users":[]}
    if len(users) > 0:
        for user in users:
            _u = dict(user)
            if _u.get('last_login_time'):
                _u['last_login_time'] = _u.get('last_login_time').strftime('%Y-%m-%d %H:%M:%S')
            if _u.get('create_time'):
                _u['create_time'] = _u.get('create_time').strftime("%Y-%m-%d %H:%M:%S")
            _users['users'].append(_u)
        return _users

def posts_to_dict(posts):
    _posts = {"posts":[]}
    if len(posts) > 0:
        for post in posts:
            _p = dict(post)
            if _p.get('create_time'):
                _p['create_time'] = _p['create_time'].strftime("%Y-%m-%d %H:%M:%S")
            if _p.get('last_update_time'):
                _p['last_update_time'] = _p.get('last_update_time').strftime('%Y-%m-%d %H:%M:%S')
            _posts['posts'].append(_p)
        return _posts

def comments_to_dict(comments):
    _comments = {"comments":[]}
    if len(comments):
        for comment in comments:
            _c = dict(comment)
            if _c.get("last_update_time"):
                _c['last_update_time'] = _c['last_update_time'].strftime('%Y-%m-%d %H:%M:%S')
                _comments['comments'].append(_c)
        return _comments





