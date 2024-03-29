from fastapi import FastAPI

app = FastAPI()


# @app.get("/")
# async def root():
#     return {"success": True, "message": "Hello World"}


@app.get("/api/ping")
async def ping():
    return {"success": True}

