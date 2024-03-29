from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


app = FastAPI()


# @app.get("/")
# async def root():
#     return {"success": True, "message": "Hello World"}


@app.get("/api/ping")
async def ping():
    return {"success": True}


app.mount("/", StaticFiles(directory="../public"), name="")
