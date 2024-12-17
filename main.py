import uvicorn
from fastapi import FastAPI
from api.todo_routing import router as todo_router
from api.auth_routing import auth_router
from tortoise.contrib.fastapi import register_tortoise
from settings.configuration import Config

app = FastAPI()

app.include_router(auth_router)

app.include_router(todo_router)

register_tortoise(
    app=app,
    db_url=Config.DB_CONNECTION,
    modules={"models": Config.DB_MODELS},
    add_exception_handlers=True,
    generate_schemas=False,
)

if __name__ == "__main__":
    uvicorn.run("todo.main:app")
