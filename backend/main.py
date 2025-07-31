from fastapi import FastAPI
from .database import engine, Base
from .routers import users, pocs, applications, comments, reviews, token

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Routers
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(pocs.router, prefix="/pocs", tags=["pocs"])
app.include_router(applications.router, prefix="/applications", tags=["applications"])
app.include_router(comments.router, prefix="/comments", tags=["comments"])
app.include_router(reviews.router, prefix="/reviews", tags=["reviews"])
app.include_router(token.router, prefix="", tags=["token"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the POC Recruitment Platform"}
