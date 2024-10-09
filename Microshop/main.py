import uvicorn
from pydantic import EmailStr, BaseModel
from fastapi import FastAPI

app = FastAPI()


class CreateUser(BaseModel):
    email: EmailStr


@app.get("/")
def root():
    return {"message": "Hello index"}


@app.get("/hello/")
def say_hello(name: str = 'World'):
    return {"message": f"Hello {name.strip().title()}!"}


@app.post('users/')
def create_user(user: CreateUser):
    return {
        'message': 'success',
        'email': user.email
    }


@app.post('/calc/add/')
def add(a: int, b: int):
    return {
        'a': a,
        'b': b,
        'result': a + b
    }


@app.get('/items/')
def list_items():
    return ['item_1', 'item_2', ]


@app.get('items/latest')
def get_latest_item():
    return {'item': {'id': 'latest'}}


@app.get('/items/{item_id}')
def get_item_id(item_id: int):
    return {'item': {'id': item_id}}


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
