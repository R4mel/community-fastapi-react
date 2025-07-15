from fastapi import FastAPI, Depends, HTTPException, Request, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.models import Post, User, Comment, Category, CategoryStatus
from app.database import get_db
from sqlalchemy import func
import httpx
import os
from app.schemas import (
    UserResponse,
    UserCreate,
    UserUpdate,
    PostResponse,
    PostCreate,
    PostUpdate,
    CommentResponse,
    CommentCreate,
    CommentUpdate,
    KakaoToken,
    CategoryResponse,
    CategoryCreate,
    CategoryUpdate,
    CategoryBase,
)
from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional

# OAuth2 configuration
security = HTTPBearer()

# JWT settings
SECRET_KEY = "QbHVQZNLI0zOluOrXAyEp96FDaEu+hPgi5gFdl8VCF8="  # 실제 운영환경에서는 환경변수로 관리
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

app = FastAPI()

# CORS 설정 추가
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    auth: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        token = auth.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.user_id == user_id).first()
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.get("/")
def read_root():
    return {"message": "Hello World"}


# --- USER CRUD ---
@app.get("/api/users/{user_id}", response_model=UserResponse)
def get_user_profile(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.put("/api/users/{user_id}", response_model=UserResponse)
def update_user_info(
    user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)
):
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


@app.post("/api/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


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
async def create_post(
    post: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    db_post = Post(**post.model_dump(), user_id=current_user.user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


# --- COMMENT CRUD ---
@app.put("/api/comments/{comment_id}", response_model=CommentResponse)
def update_comment(
    comment_id: int, comment_update: CommentUpdate, db: Session = Depends(get_db)
):
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


@app.post("/api/posts/{post_id}/comments", response_model=CommentResponse)
async def create_comment(
    post_id: int,
    comment: CommentCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    # Check if post exists
    post = db.query(Post).filter(Post.post_id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    db_comment = Comment(
        **comment.model_dump(), post_id=post_id, user_id=current_user.user_id
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


@app.get("/api/posts/{post_id}/comments", response_model=list[CommentResponse])
def get_post_comments(post_id: int, db: Session = Depends(get_db)):
    comments = db.query(Comment).filter(Comment.post_id == post_id).all()
    return comments


@app.delete("/api/posts/{post_id}/comments/{comment_id}")
async def delete_comment(
    post_id: int,
    comment_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    comment = (
        db.query(Comment)
        .filter(Comment.comment_id == comment_id, Comment.post_id == post_id)
        .first()
    )

    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    if comment.user_id != current_user.user_id:
        raise HTTPException(
            status_code=403, detail="Not authorized to delete this comment"
        )

    db.delete(comment)
    db.commit()
    return {"detail": "Comment deleted"}


@app.get("/api/users/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user


# Kakao OAuth endpoints
@app.get("/api/auth/kakao/url")
async def get_kakao_url():
    scope = os.getenv("KAKAO_SCOPE", "profile_nickname,profile_image")
    return {
        "url": f"{os.getenv('KAKAO_AUTH_URI')}?client_id={os.getenv('KAKAO_CLIENT_ID')}&redirect_uri={os.getenv('KAKAO_REDIRECT_URI')}&response_type=code&scope={scope}"
    }


@app.post("/api/auth/kakao")
async def kakao_login(token: KakaoToken, db: Session = Depends(get_db)):
    try:
        print(f"[Backend] Starting Kakao login process with code: {token.code}")

        # Exchange authorization code for access token
        token_request_data = {
            "grant_type": "authorization_code",
            "client_id": os.getenv("KAKAO_CLIENT_ID"),
            "client_secret": os.getenv("KAKAO_CLIENT_SECRET"),
            "code": token.code,
            "redirect_uri": os.getenv("KAKAO_REDIRECT_URI"),
        }

        print(f"[Backend] Token request data: {token_request_data}")

        async with httpx.AsyncClient() as client:
            # Get access token
            token_response = await client.post(
                "https://kauth.kakao.com/oauth/token", data=token_request_data
            )

            print(f"[Backend] Token response status: {token_response.status_code}")
            print(f"[Backend] Token response body: {token_response.text}")

            if not token_response.is_success:
                raise HTTPException(
                    status_code=400,
                    detail=f"Failed to get access token from Kakao: {token_response.text}",
                )

            token_data = token_response.json()
            access_token = token_data.get("access_token")

            if not access_token:
                raise HTTPException(
                    status_code=400, detail="No access token in Kakao response"
                )

            # Get user info
            headers = {"Authorization": f"Bearer {access_token}"}
            user_response = await client.get(
                "https://kapi.kakao.com/v2/user/me", headers=headers
            )

            print(f"[Backend] User info response status: {user_response.status_code}")
            print(f"[Backend] User info response body: {user_response.text}")

            if not user_response.is_success:
                raise HTTPException(
                    status_code=400,
                    detail=f"Failed to get user info from Kakao: {user_response.text}",
                )

            # Get user info from Kakao and create or update user
            user_info = user_response.json()
            kakao_id = str(user_info["id"])
            kakao_account = user_info.get("kakao_account", {})
            profile = kakao_account.get("profile", {})

            # Check if user exists
            user = db.query(User).filter(User.social_id == kakao_id).first()

            if not user:
                # Create new user
                user = User(
                    social_id=kakao_id,
                    nickname=profile.get("nickname", "Anonymous"),
                    profile_image=profile.get("profile_image_url"),
                )
                db.add(user)
                db.commit()
                db.refresh(user)

            # Generate JWT access token
            access_token = create_access_token(
                data={"sub": str(user.user_id)},
                expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
            )

            return {
                "user": {
                    "user_id": user.user_id,
                    "nickname": user.nickname,
                    "profile_image": user.profile_image,
                    "is_admin": user.is_admin,
                    "total_points": user.total_points,
                },
                "access_token": access_token,
            }

    except HTTPException as he:
        print(f"[Backend] HTTP Exception: {he.detail}")
        raise he
    except Exception as e:
        print(f"[Backend] Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error during Kakao login: {str(e)}",
        )


@app.get("/api/auth/kakao/callback")
async def kakao_callback(code: str, db: Session = Depends(get_db)):
    # Exchange authorization code for access token
    token_request_data = {
        "grant_type": "authorization_code",
        "client_id": os.getenv("KAKAO_CLIENT_ID"),
        "client_secret": os.getenv("KAKAO_CLIENT_SECRET"),
        "code": code,
        "redirect_uri": os.getenv("KAKAO_REDIRECT_URI"),
    }

    async with httpx.AsyncClient() as client:
        token_response = await client.post(
            os.getenv("KAKAO_TOKEN_URI"), data=token_request_data
        )
        token_response.raise_for_status()
        token_data = token_response.json()

        # Get user info from Kakao
        headers = {"Authorization": f"Bearer {token_data['access_token']}"}
        user_info_response = await client.get(
            os.getenv("KAKAO_USER_INFO_URI"), headers=headers
        )
        user_info_response.raise_for_status()
        kakao_user_info = user_info_response.json()

    # Find or create user
    kakao_id = str(kakao_user_info["id"])
    user = db.query(User).filter(User.social_id == kakao_id).first()

    if not user:
        user = User(
            social_id=kakao_id,
            nickname=kakao_user_info["properties"]["nickname"],
            profile_image=kakao_user_info["properties"].get("profile_image", None),
            is_active=True,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    # Create access token for our API
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.user_id}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


# --- Category CRUD ---
@app.get("/api/categories", response_model=list[CategoryResponse])
async def get_categories(db: Session = Depends(get_db)):
    try:
        categories = []
        for status in CategoryStatus:
            category = (
                db.query(Category).filter(Category.category_status == status).first()
            )
            if not category:
                # Create category if it doesn't exist
                category = Category(category_status=status)
                db.add(category)
                db.commit()
                db.refresh(category)
            categories.append(category)
        return categories
    except Exception as e:
        print(f"Error in get_categories: {str(e)}")  # 디버깅을 위한 로그
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/categories/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.category_id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@app.post("/api/categories", response_model=CategoryResponse)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    db_category = Category(**category.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


@app.put("/api/categories/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int, category: CategoryUpdate, db: Session = Depends(get_db)
):
    db_category = db.query(Category).filter(Category.category_id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    update_data = category.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_category, key, value)
    db.commit()
    db.refresh(db_category)
    return db_category


@app.delete("/api/categories/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.category_id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(category)
    db.commit()
    return {"detail": "Category deleted"}
