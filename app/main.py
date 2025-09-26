# app/main.py
from fastapi import FastAPI, HTTPException, status
from .schemas import User

app = FastAPI()
users: list[User] = []

@app.get("/hello")
def hello():
    return {"message": "Hello, World!"}

@app.get("/api/users")
def get_users():
    return users

@app.get("/api/users/{user_id}")
def get_user(user_id: int):
    for u in users:
        if u.user_id == user_id:
            return u
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

@app.post("/api/users", status_code=status.HTTP_201_CREATED)
def add_user(user: User):
    if any(u.user_id == user.user_id for u in users):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="user_id already exists")
    users.append(user)
    return user

#reflection questions
#1 comes from validation problems like if the name is too short or too long, if the email isn't the right format, or if the age is too young ayo
#2 201 useful as it lets you know that a new entry was created, 404 is good as it shows something wasn't found or doesn't exist
#3 the layout helps as more endpoints can easily be added and tested using swagger. Validation logic can also just be added into the cshemas

@app.put("/api/users/{user_id}", status_code=status.HTTP_201_CREATED)
def update_user(user_id: int, updated_user: User):
    for i, user in enumerate(users):
        if user.user_id == user_id:
            users[i] = updated_user
            return updated_user
    if any(user.user_id == updated_user.user_id for user in users):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="user_id already exists")
    
    
@app.delete("/api/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    for user in users:
        if user.user_id == user_id:
            users.remove(user)
            return users
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@app.get("/health")
def health():
    return {"status": "ok"}

