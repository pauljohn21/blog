

Auth = {
    "select_user" : "select * from users where username = $1",
    "login_update":"update users set last_login_time = $1 where id = $2",
    "register_insert":"insert into users (username,password,create_time,last_login_time) values ($1,$2,$3,$4)",
    "select_user_profile": "select u.username,u.location,u.last_login_time,u.levemessage from users u where id = $1",
    "update_user_profile":"update users set location=$1,levemessage=$2 where id = $3 "
}
API = {
    "get_users":"select u.id,u.username,u.location,u.levemessage,u.last_login_time from users u",
    "get_user":"select u.id,u.username,u.location,u.levemessage,u.last_login_time from users u id = $1"
}

Main = {
    "select_author":"select author_id from posts where id = $1",
    "home_select":"select * from posts order by last_update_time desc",
    "post_del":"delete from posts where id = $1",
    "post_select":"select * from posts where id = $1",
    "post_update":"update posts set post = $1,post_title = $2,tag = $3,last_update_time = $4 where id = $5",
    "create_post":"insert into posts (post_title,post,author_id,create_time,last_update_time,tag) values ($1,$2,$3,$4,$5,$6)"
}










