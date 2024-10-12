from fastapi import APIRouter

app = APIRouter()


@app.get("")
async def health_check():
    return {"status": "healthy"}