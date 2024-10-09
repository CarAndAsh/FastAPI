from users.schemas import CreateUser


def create_user(user_in: CreateUser):
    user = user_in.model_dump()
    return {
        'message': 'success',
        'user': {
            'username': user_in.username,
            'email': user_in.email
        }
    }
