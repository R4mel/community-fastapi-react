from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from models import Post, User, Comment
from database import get_db
from sqlalchemy import func
from schemas import UserResponse, UserUpdate, PostResponse, PostUpdate, PostCreate, CommentResponse, CommentUpdate, CommentCreate

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- USER CRUD ---
@app.get("/api/users/{user_id}", response_model=UserResponse)
def get_user_profile(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/api/users/{user_id}", response_model=UserResponse)
def update_user_info(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    update_data = user_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user

@app.delete("/api/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"detail": "User deleted"}

# --- POST CRUD ---
@app.get("/api/posts/{post_id}", response_model=PostResponse)
def get_post_by_id(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.post_id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@app.put("/api/posts/{post_id}", response_model=PostResponse)
def update_post(post_id: int, post_update: PostUpdate, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.post_id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    update_data = post_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(post, key, value)
    db.commit()
    db.refresh(post)
    return post

@app.delete("/api/posts/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.post_id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(post)
    db.commit()
    return {"detail": "Post deleted"}

@app.get("/api/posts", response_model=list[PostResponse])
def get_posts(keyword: str = "", category_id: int = -1, db: Session = Depends(get_db)):
    query = db.query(Post)
    if keyword:
        query = query.filter(func.lower(Post.title).like(f"%{keyword.lower()}%"))  # type: ignore
    if category_id != -1:
        query = query.filter(Post.category_id == category_id)  # type: ignore
    return query.all()

@app.post("/api/posts", response_model=PostResponse)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    db_post = Post(**post.model_dump())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

# --- COMMENT CRUD ---
@app.put("/api/comments/{comment_id}", response_model=CommentResponse)
def update_comment(comment_id: int, comment_update: CommentUpdate, db: Session = Depends(get_db)):
    comment = db.query(Comment).filter(Comment.comment_id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    update_data = comment_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(comment, key, value)
    db.commit()
    db.refresh(comment)
    return comment

@app.delete("/api/comments/{comment_id}")
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    comment = db.query(Comment).filter(Comment.comment_id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    db.delete(comment)
    db.commit()
    return {"detail": "Comment deleted"}

@app.get("/api/posts/{post_id}/comments", response_model=list[CommentResponse])
def get_comments_by_post(post_id: int, db: Session = Depends(get_db)):
    return db.query(Comment).filter(Comment.post_id == post_id).all()

@app.post("/api/posts/{post_id}/comments", response_model=CommentResponse)
def create_comment(post_id: int, comment: CommentCreate, db: Session = Depends(get_db)):
    db_comment = Comment(**comment.model_dump(), post_id=post_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment