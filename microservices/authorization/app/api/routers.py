from fastapi import APIRouter

app = APIRouter()

@app.get("/{user_id}")
def get_user(user_id: int):
    pass