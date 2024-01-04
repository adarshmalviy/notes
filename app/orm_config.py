import os

from fastapi import FastAPI
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise
from app.config import database_url


DATABASE_URL = database_url
# Construct the database URL
print("URL:", DATABASE_URL)

TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "models": {
            "models": ["app.database.models", "aerich.models"],  # Replace with your actual model location
            "default_connection": "default",
        }
    },
}


def init_db(app: FastAPI) -> None:
    ##Tortoise.init_models(["models"], "models")
    register_tortoise(
        app,
        config=TORTOISE_ORM,
        generate_schemas=True,
        add_exception_handlers=True,
    )


async def init_tortoise():
    await Tortoise.init(config=TORTOISE_ORM)


async def close_db():
    await Tortoise.close_connections()
