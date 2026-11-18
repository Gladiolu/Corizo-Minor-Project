from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from database import SessionLocal, engine
from models import Base, Student

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home(request: Request):
    db = SessionLocal()
    students = db.query(Student).all()

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "students": students
        }
    )


@app.get("/add")
def add_page(request: Request):
    return templates.TemplateResponse(
        "add.html",
        {"request": request}
    )


@app.post("/add")
def add_student(
    name: str = Form(...),
    email: str = Form(...),
    course: str = Form(...)
):
    db = SessionLocal()

    student = Student(
        name=name,
        email=email,
        course=course
    )

    db.add(student)
    db.commit()

    return RedirectResponse("/", status_code=303)


@app.get("/edit/{student_id}")
def edit_page(student_id: int, request: Request):
    db = SessionLocal()

    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    return templates.TemplateResponse(
        "edit.html",
        {
            "request": request,
            "student": student
        }
    )


@app.post("/edit/{student_id}")
def update_student(
    student_id: int,
    name: str = Form(...),
    email: str = Form(...),
    course: str = Form(...)
):
    db = SessionLocal()

    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    student.name = name
    student.email = email
    student.course = course

    db.commit()

    return RedirectResponse("/", status_code=303)


@app.get("/delete/{student_id}")
def delete_student(student_id: int):
    db = SessionLocal()

    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    db.delete(student)
    db.commit()

    return RedirectResponse("/", status_code=303)