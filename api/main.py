from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"success": True, "message": "Hello World"}


@app.get("/ping")
async def ping():
    return {"success": True}

