from fastapi import FastAPI
from .database import engine, Base
from .routers import users, pocs, applications, comments, reviews, token

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(pocs.router)
app.include_router(applications.router)
app.include_router(comments.router)
app.include_router(reviews.router)
app.include_router(token.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the POC Recruitment Platform"}
