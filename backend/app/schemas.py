from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

from models import CategoryStatus

class UserBase(BaseModel):
    social_id: str = Field(..., description="Social login ID")
    nickname: str = Field(..., description="User nickname")
    profile_image: Optional[str] = Field(None, description="Profile image URL")
    is_admin: bool = Field(False, description="Admin status")
    total_points: int = Field(0, description="Total points")


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    nickname: Optional[str] = None
    profile_image: Optional[str] = None
    total_points: Optional[int] = None


class CategoryBase(BaseModel):
    category_status: CategoryStatus = Field(..., description="Category status")


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    pass


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


class CommentBase(BaseModel):
    content: str = Field(..., description="Comment content")


class CommentCreate(CommentBase):
    post_id: int = Field(..., description="Post ID")


class CommentUpdate(CommentBase):
    pass


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

class UserResponse(BaseModel):
    user_id: int
    social_id: str
    nickname: str
    profile_image: Optional[str] = None
    is_admin: bool = False
    total_points: int = 0
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class CategoryResponse(BaseModel):
    category_id: int
    category_status: CategoryStatus
    
    class Config:
        from_attributes = True


class PostImageResponse(BaseModel):
    post_image_id: int
    post_id: int
    image_url: Optional[str] = None
    original_filename: Optional[str] = None
    
    class Config:
        from_attributes = True


class CommentResponse(BaseModel):
    comment_id: int
    post_id: int
    user_id: int
    content: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class PostResponse(BaseModel):
    post_id: int
    title: str
    content: str
    user_id: int
    category_id: int
    created_at: datetime
    updated_at: datetime
    view_count: int
    
    class Config:
        from_attributes = True


class PostDetailResponse(PostResponse):
    user: UserResponse
    category: CategoryResponse
    post_images: List[PostImageResponse] = []
    comments: List[CommentResponse] = []
    likes_count: int = 0
    
    class Config:
        from_attributes = True


class LikeResponse(BaseModel):
    user_id: int
    post_id: int
    is_liked: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


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