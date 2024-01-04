import os
import uvicorn

from app.main import create_app
from app.orm_config import close_db, init_db, init_tortoise

app = create_app()

@app.on_event("startup")
async def startup_event():
    print("Starting up...")
    await init_tortoise()
    # print("Init Done...")
    init_db(app)
    
    # print("DB connection done...")
    # command = AerichCommand(tortoise_config=TORTOISE_ORM)
    # await command.init()


@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down...")


if __name__ == "__main__":
    uvicorn.run("__main__:app", port=int(os.environ.get("PORT", 8080)), host="0.0.0.0", reload=True)
