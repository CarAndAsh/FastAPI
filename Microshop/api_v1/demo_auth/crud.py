from auth import utils as auth_utils
from users.schemas import UserSchema

max = UserSchema(username='max', password=auth_utils.hash_password('pass'), email='max@examp.le')
zack = UserSchema(username='zack', password=auth_utils.hash_password('word'))
user_db: dict[str, UserSchema] = {
    max.username: max,
    zack.username: zack
}
