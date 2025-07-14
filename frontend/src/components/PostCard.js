import React from 'react';
import { Link } from 'react-router-dom';

const PostCard = ({ post }) => (
  <div className="card post-card h-100">
    <div className="card-body">
      <h5 className="card-title">{post.title}</h5>
      <p className="card-text text-muted">
        {post.content.length > 100 ? post.content.slice(0, 100) + '...' : post.content}
      </p>
      <div className="d-flex justify-content-between align-items-center">
        <small className="text-muted">
          {post.created_at ? new Date(post.created_at).toLocaleString('ko-KR', { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' }) : ''}
        </small>
        <span className="badge bg-secondary">{post.authorNickname || '익명'}</span>
      </div>
    </div>
    <div className="card-footer">
      <div className="d-flex justify-content-between align-items-center">
        <small className="text-muted">조회수: {post.view_count}</small>
        <Link to={`/posts/${post.post_id}`} className="btn btn-sm btn-outline-primary">자세히 보기</Link>
      </div>
    </div>
  </div>
);

export default PostCard; 