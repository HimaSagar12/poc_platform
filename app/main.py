from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.database import engine, Base
from app.routers import users, pocs, applications, comments, reviews, notifications

Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS Middleware
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(pocs.router, prefix="/pocs", tags=["pocs"])
app.include_router(applications.router, prefix="/applications", tags=["applications"])
app.include_router(comments.router, tags=["comments"])
app.include_router(reviews.router, prefix="/reviews", tags=["reviews"])
app.include_router(notifications.router, prefix="/notifications", tags=["notifications"])
