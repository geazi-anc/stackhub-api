from fastapi import FastAPI, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from models.user import User
from models.question import Question
from services.question import QuestionServices
from services.user import UserServices
from pydantic import BaseModel


# settings
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# load enviroment variables from .env file
load_dotenv()

# create instances of services
question_services = QuestionServices()
user_services = UserServices()


@app.get("/ping")
def ping():
    return "PONG!"


@app.post("/user", status_code=201)
def user_save(email: str = Form(...), password: str = Form(...), first_name: str = Form(...), last_name: str = Form(...)):
    user = User(first_name=first_name, last_name=last_name,
                email=email, password=password)
    user_services.save(user)

    return "User has been succesfully created!"


@app.get("/user/{id}")
def user_find_by(id: str):
    return user_services.find_by(filter={"_id": id})


@app.post("/login")
def user_login(email: str = Form(...), password: str = Form(...)):
    user = user_services.find_by({"email": email})

    if user["password"] != password:
        raise HTTPException(
            status_code=403, detail="Invalid Password for this user.")

    return {"id": user["_id"], "first_name": user["first_name"], "last_name": user["last_name"]}


@app.post("/question", status_code=201)
def question_save(question: Question):
    question_services.save(question)

    return "Question has been succesfully sent!"


@app.get("/question")
def question_find_all():
    questions = question_services.find_all()
    return questions


@app.get("/question/{id}")
def question_find_by_id(id: str):
    return question_services.find_by({"_id": id})
