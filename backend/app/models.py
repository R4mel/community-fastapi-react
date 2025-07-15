from enum import Enum
from datetime import datetime
from sqlalchemy import VARCHAR, Boolean, Column, DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship
from sqlalchemy import Enum as SQLEnum
from app.database import Base


class CategoryStatus(str, Enum):
    FREE = "FREE"
    TIP = "TIP"
    QUESTION = "QUESTION"

    @property
    def description(self) -> str:
        descriptions = {
            CategoryStatus.FREE: "자유게시판",
            CategoryStatus.TIP: "팁게시판",
            CategoryStatus.QUESTION: "질문게시판",
        }
        return descriptions[self]


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    social_id = Column(VARCHAR(255), nullable=False, unique=True, index=True)
    nickname = Column(VARCHAR(255), nullable=False)
    profile_image = Column(VARCHAR, nullable=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.now, onupdate=datetime.now, nullable=False
    )
    is_admin = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)  # 추가: 계정 활성화 상태
    total_points = Column(Integer, default=0, nullable=False)

    # Relationships
    posts = relationship("Post", back_populates="user", cascade="all, delete-orphan")
    comments = relationship(
        "Comment", back_populates="user", cascade="all, delete-orphan"
    )
    likes = relationship("Like", back_populates="user", cascade="all, delete-orphan")


class Category(Base):
    __tablename__ = "categories"

    category_id = Column(Integer, primary_key=True, index=True)
    category_status = Column(SQLEnum(CategoryStatus), nullable=False)

    # Relationships
    posts = relationship(
        "Post", back_populates="category", cascade="all, delete-orphan"
    )


class Post(Base):
    __tablename__ = "posts"

    post_id = Column(Integer, primary_key=True, index=True)
    title = Column(VARCHAR(255), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.now, onupdate=datetime.now, nullable=False
    )
    view_count = Column(Integer, default=0, nullable=False)

    # Foreign Keys
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.category_id"), nullable=False)

    # Relationships
    user = relationship("User", back_populates="posts")
    category = relationship("Category", back_populates="posts")
    post_images = relationship(
        "PostImage", back_populates="post", cascade="all, delete-orphan"
    )
    comments = relationship(
        "Comment", back_populates="post", cascade="all, delete-orphan"
    )
    likes = relationship("Like", back_populates="post", cascade="all, delete-orphan")

    def increase_view_count(self):
        """Increase view count by 1"""
        self.view_count += 1

    def update(self, title: str, content: str, category_id: int):
        """Update post information"""
        self.title = title
        self.content = content
        self.category_id = category_id
        self.updated_at = datetime.utcnow()


class Comment(Base):
    __tablename__ = "comments"

    comment_id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.now, onupdate=datetime.now, nullable=False
    )

    # Foreign Keys
    post_id = Column(Integer, ForeignKey("posts.post_id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)

    # Relationships
    post = relationship("Post", back_populates="comments")
    user = relationship("User", back_populates="comments")

    def update_content(self, content: str):
        """Update comment content"""
        self.content = content
        self.updated_at = datetime.utcnow()


class PostImage(Base):
    __tablename__ = "post_images"

    post_image_id = Column(Integer, primary_key=True, index=True)
    image_url = Column(Text, nullable=True)
    original_filename = Column(VARCHAR(255), nullable=True)

    # Foreign Keys
    post_id = Column(Integer, ForeignKey("posts.post_id"), nullable=False)

    # Relationships
    post = relationship("Post", back_populates="post_images")


class Like(Base):
    __tablename__ = "likes"

    # Composite primary key
    user_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.post_id"), primary_key=True)

    is_liked = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)

    # Relationships
    user = relationship("User", back_populates="likes")
    post = relationship("Post", back_populates="likes")
