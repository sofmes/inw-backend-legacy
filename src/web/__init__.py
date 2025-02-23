from fastapi import FastAPI

from web.auth import router as auth_router
from web.helper.lifespan import lifespan
from web.me import router as me_router

app = FastAPI(lifespan=lifespan)


@app.get("/")
def root() -> str:
    return "'Hello, world!' from sofmes"


app.include_router(auth_router)
app.include_router(me_router)
