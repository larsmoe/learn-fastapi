from ast import Dict
from fastapi import FastAPI, status, HTTPException, Depends, Response, APIRouter
from typing import List, Optional 
from sqlalchemy import func
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(prefix='/posts', tags=['Posts'])

@router.get("/", response_model=List[schemas.PostOut]) #, response_model=List[schemas.PostRespose]
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    #posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all() (if it is only enabled to see own posts)
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() (just for reference before votes)
    posts = db.query(models.Post, func.count(models.Vote.post_id).label('votes')
                       ).join(models.Vote, models.Vote.post_id == models.Post.id, isouter = True
                       ).group_by(models.Post.id
                       ).filter(models.Post.title.contains(search)
                       ).limit(limit
                       ).offset(skip
                       ).all()
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostRespose)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id = current_user.id, **post.dict()) #**post.model_dump() for newer fastapi versions
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: Dict = Depends(oauth2.get_current_user)):
    post = db.query(models.Post, func.count(models.Vote.post_id).label('votes')
                       ).join(models.Vote, models.Vote.post_id == models.Post.id, isouter = True
                       ).group_by(models.Post.id
                       ).filter(models.Post.id == id
                       ).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id {id} not found')
    #if post.owner_id != current_user.id: (if it is only enabled to see own posts)
    #    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Hurensohn, schau nicht die Posts von anderen an!")
    return post

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id {id} does not exist, Hurensohn!')
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Hurensohn, lösch nicht die Posts von anderen!")
    post_query.delete(synchronize_session = False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put('/{id}', response_model=schemas.PostRespose)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_updated = post_query.first()
    if not post_updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id {id} does not exist, Hurensohn!')
    if post_updated.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Hurensohn, update nicht die Posts von anderen!")
    post_query.update(post.model_dump(), synchronize_session = False)
    db.commit()
    return post_query.first()


'''
Here are all API Calls with pure SQL instead of SQLAlchemy, just here for information purposes:
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
@app.get("/posts")
def get_posts():
    posts = cursor.execute("""SELECT * FROM posts""").fetchall()
    print(posts)
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    new_post = cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published)).fetchone()
    conn.commit()
    return {"data": new_post}

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),)).fetchone()
    print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id {id} not found')
    return {"post_detail": post}

@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    deleted_post = cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id), )).fetchone()
    conn.commit()
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id {id} does not exist, Hurensohn!')
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put('/posts/{id}')
def update_post(id: int, post: Post):
    updated_post = cursor.execute("""UPDATE  posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", 
                                  (post.title, post.content, post.published, str(id))).fetchone()
    conn.commit()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id {id} does not exist, Hurensohn!')
    return {'data': updated_post}

'''