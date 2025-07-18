from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from api.modules.users import users_routes
from api.modules.agents import agents_routes

from core.dependencies.configure_container import configure_container

@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_container()  
    yield

app = FastAPI(lifespan=lifespan)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(users_routes.router)
app.include_router(agents_routes.router)

