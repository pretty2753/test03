# main.py

from fastapi import Depends, FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import text
from sqlalchemy.orm import Session
from database import get_db


# FastAPI 객체 생성
app = FastAPI()
# Jinja2 템플릿 객체 생성
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "fortuneToday": "동쪽으로 가면 귀인을 만나요"
        }
    )


# GET 방식 /post 요청 처리 (글 목록)
@app.get("/post", response_class=HTMLResponse)
def getPosts(request: Request, db: Session = Depends(get_db)):
    query = text("""
        SELECT num, writer, title, content, created_at
        FROM post
        ORDER BY num DESC
    """)
    result = db.execute(query)
    posts = result.fetchall()
    
    return templates.TemplateResponse(
        request=request,
        name="post/list.html",
        context={
            "posts": posts
        }
    )


# GET 방식 - 글 작성 폼
@app.get("/post/new", response_class=HTMLResponse)
def getNewForm(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name="post/new-form.html"
    )


# POST 방식 - 글 저장
@app.post("/post/new")
def createPost(
    writer: str = Form(...),
    title: str = Form(...), 
    content: str = Form(...),
    db: Session = Depends(get_db)
):
    query = text("""
        INSERT INTO post (writer, title, content)
        VALUES (:writer, :title, :content)
    """)
    db.execute(query, {"writer": writer, "title": title, "content": content})
    db.commit()
    
#삭제 기능
@app.post("/post/delete/{num}")
def deletePost(num: int, db: Session = Depends(get_db)):
    query = text("DELETE FROM post WHERE num = :num")
    db.execute(query, {"num": num})
    db.commit()
    
    return RedirectResponse("/post", status_code=302)