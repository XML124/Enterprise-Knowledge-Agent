from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.routes import router
from app.core.config import get_settings
from app.core.logging import configure_logging
from app.db.schema import initialise_database

settings = get_settings()
configure_logging(settings.log_level)

@asynccontextmanager
async def lifespan(app: FastAPI):
    initialise_database()
    yield

app = FastAPI(title="Enterprise Knowledge Agent", version="0.1.0", lifespan=lifespan)
app.include_router(router)
