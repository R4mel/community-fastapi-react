import React from 'react';
import { Link } from 'react-router-dom';

const PostCard = ({ post }) => (
  <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition duration-300">
    <div className="flex items-center gap-3 mb-2">
      <span className="px-3 py-1 text-sm font-medium bg-blue-100 text-blue-800 rounded-full">
        {post.category?.status || '카테고리 없음'}
      </span>
    </div>
    <h3 className="text-xl font-semibold mb-2">{post.title}</h3>
    <p className="text-gray-600 mb-4">
      {post.content.length > 100 ? post.content.slice(0, 100) + '...' : post.content}
    </p>
    <div className="flex justify-between items-center mb-4">
      <div className="flex items-center space-x-2">
        <img
          src={post.user?.profile_image || '/default-avatar.png'}
          alt={post.user?.nickname || '익명'}
          className="w-6 h-6 rounded-full"
        />
        <span className="text-sm text-gray-700">{post.user?.nickname || '익명'}</span>
      </div>
      <span className="text-sm text-gray-500">
        {post.created_at ? new Date(post.created_at).toLocaleString('ko-KR', { 
          year: 'numeric', 
          month: '2-digit', 
          day: '2-digit', 
          hour: '2-digit', 
          minute: '2-digit' 
        }) : ''}
      </span>
    </div>
    <div className="flex justify-between items-center">
      <span className="text-sm text-gray-500">조회수: {post.view_count || 0}</span>
      <Link 
        to={`/posts/${post.post_id}`} 
        className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition duration-300"
      >
        자세히 보기
      </Link>
    </div>
  </div>
);

export default PostCard;