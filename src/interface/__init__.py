from fastapi import FastAPI

from interface.auth import router as auth_router
from interface.helper.lifespan import lifespan
from interface.me import router as me_router

app = FastAPI(lifespan=lifespan)


@app.get("/")
def root() -> str:
    return "'Hello, world!' from sofmes"


app.include_router(auth_router)
app.include_router(me_router)
