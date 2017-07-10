

Auth = {
    "select_user" : "select * from users where username = $1",
    "login_update":"update users set last_login_time = $1 where id = $2",
    "register_insert":"insert into users (username,password_hash,create_time,last_login_time) values ($1,$2,$3,$4)",
    "select_user_profile": "select u.username,u.location,u.last_login_time,u.levemessage, from users u where id = $1",
    "update_user_profile":"update users set u.location=$1,u.levemessage=$2 where id = $3 "
}
API = {
    "get_users":"select u.id,u.username,u.location,u.levemessage,u.last_login_time from users u",
    "get_user":"select u.id,u.username,u.location,u.levemessage,u.last_login_time from users u id = $1"
}










