from fastapi import FastAPI, HTTPException, Depends, status, Response, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn
from pydantic import BaseModel
from typing import List
from fastapi.staticfiles import StaticFiles
from fastapi import Form
import shutil
from pymongo import MongoClient
from scripts.auth import get_password_hash, create_access_token

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates=Jinja2Templates(directory="templates")

# MongoDB connection details
MONGO_DETAILS = "mongodb+srv://code_god:rootadmin@aoristai.1ofe1s4.mongodb.net/test"
client = MongoClient(MONGO_DETAILS)

# Select the database
db = client["athena"]

# Select the collection
users_collection = db["users"]


@app.route('/', methods=['GET'])
def home():
    
    return 



@app.post("/signup")
async def signup(email: str, password: str):
    # Check if user already exists
    existing_user = users_collection.find_one({"email": email})
    if existing_user:
        raise HTTPException(status_code=400, detail="User already registered")
    # Hash password
    hashed_password = get_password_hash(password)
    # Save user details in MongoDB
    user = {"email": email, "password": hashed_password}
    result = users_collection.insert_one(user)
    # Create JWT access token
    access_token = create_access_token(data={"sub": str(result.inserted_id)})
    return {"access_token": access_token}