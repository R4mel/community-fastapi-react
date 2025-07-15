from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from app.models import CategoryStatus


class UserBase(BaseModel):
    social_id: str = Field(..., description="Social login ID")
    nickname: str = Field(..., description="User nickname")
    profile_image: Optional[str] = Field(None, description="Profile image URL")
    is_admin: bool = Field(False, description="Admin status")
    is_active: bool = Field(True, description="Account active status")
    total_points: int = Field(0, description="Total points")


class KakaoToken(BaseModel):
    code: str = Field(..., description="Kakao authorization code")


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    nickname: Optional[str] = None
    profile_image: Optional[str] = None
    total_points: Optional[int] = None


class UserResponse(BaseModel):
    user_id: int
    social_id: str
    nickname: str
    profile_image: Optional[str] = None
    is_admin: bool = False
    is_active: bool = True  # 추가: 계정 활성화 상태
    total_points: int = 0
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CategoryBase(BaseModel):
    category_status: CategoryStatus = Field(..., description="Category status")


class CategoryCreate(CategoryBase):
    pass


class CategoryResponse(CategoryBase):
    category_id: int

    class Config:
        from_attributes = True

    def dict(self, *args, **kwargs):
        d = super().dict(*args, **kwargs)
        d["status"] = self.category_status.description if self.category_status else ""
        return d


class CategoryUpdate(CategoryBase):
    pass


class CommentBase(BaseModel):
    content: str = Field(..., description="Comment content")


class CommentCreate(CommentBase):
    pass


class CommentUpdate(CommentBase):
    pass


class CommentResponse(CommentBase):
    comment_id: int
    post_id: int
    user_id: int
    user: UserResponse
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PostBase(BaseModel):
    title: str = Field(..., description="Post title")
    content: str = Field(..., description="Post content")
    category_id: int = Field(..., description="Category ID")


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category_id: Optional[int] = None


class PostResponse(PostBase):
    post_id: int
    user_id: int
    user: UserResponse
    created_at: datetime
    updated_at: datetime
    comments: List[CommentResponse] = []

    class Config:
        from_attributes = True


class PostImageBase(BaseModel):
    image_url: Optional[str] = Field(None, description="Image URL")
    original_filename: Optional[str] = Field(None, description="Original filename")


class PostImageCreate(PostImageBase):
    post_id: int = Field(..., description="Post ID")


class PostImageUpdate(PostImageBase):
    pass


class LikeBase(BaseModel):
    is_liked: bool = Field(False, description="Like status")


class LikeCreate(LikeBase):
    user_id: int = Field(..., description="User ID")
    post_id: int = Field(..., description="Post ID")


class LikeUpdate(LikeBase):
    pass


__all__ = [
    # Pydantic request models
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "CategoryBase",
    "CategoryCreate",
    "CategoryUpdate",
    "PostBase",
    "PostCreate",
    "PostUpdate",
    "CommentBase",
    "CommentCreate",
    "CommentUpdate",
    "PostImageBase",
    "PostImageCreate",
    "PostImageUpdate",
    "LikeBase",
    "LikeCreate",
    "LikeUpdate",
    # Pydantic response models
    "UserResponse",
    "CategoryResponse",
    "PostResponse",
    "PostDetailResponse",
    "CommentResponse",
    "PostImageResponse",
    "LikeResponse",
]
