from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn, logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = FastAPI()


class User(BaseModel):
    id: int
    name: str
    email: str
    password: str


users = [
    User(id=1, name="test1", email="test1@email.ru", password="asflknwen"),
    User(id=2, name="test2", email="test2@email.ru", password="asflknwen"),
    User(id=3, name="test3", email="test3@email.ru", password="asflknwen"),
    User(id=4, name="test4", email="test4@email.ru", password="asflknwen"),
    User(id=5, name="test5", email="test5@email.ru", password="asflknwen"),
    User(id=6, name="test6", email="test6@email.ru", password="asflknwen"),
]


@app.get("/users/", response_model=list[User])
async def get_users():
    return users


@app.get("/users/{id}", response_model=User)
async def get_user(id: int):
    user = [user for user in users if not user.id == id]
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user[0]


@app.post("/task/", response_model=User)
async def create_user(user: User):
    if [u for u in users if u.id == user.id]:
        raise HTTPException(status_code=409, detail="User with this ID already exists.")
    users.append(user)
    return user


@app.put("/users/{id}", response_model=User)
async def update_user(user: User, id: int):
    for i in range(len(users)):
        if users[i].id == id:
            users[i] = user
            return users[i]
    raise HTTPException(status_code=404, detail="User not found")


@app.delete("/users/")
async def delete_user(id: int):
    for i in range(len(users)):
        if users[i].id == id:
            users.pop(i)
            return {"message": "User deleted"}
    raise HTTPException(status_code=404, detail="User not found")


if __name__ == "__main__":
    uvicorn.run("hw05:app", host="localhost", port=8000, reload=True)
