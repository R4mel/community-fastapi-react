import React, { useEffect, useState } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import CommentList from '../components/CommentList';
import CommentForm from '../components/CommentForm';

const PostDetailPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [post, setPost] = useState(null);
  const [comments, setComments] = useState([]);

  useEffect(() => {
    fetch(`/api/posts/${id}`)
      .then(res => res.json())
      .then(setPost);
    fetch(`/api/posts/${id}/comments`)
      .then(res => res.json())
      .then(setComments);
  }, [id]);

  const handleDelete = () => {
    if (window.confirm('정말 삭제하시겠습니까?')) {
      fetch(`/api/posts/${id}`, { method: 'DELETE' })
        .then(() => navigate('/posts'));
    }
  };

  const handleCommentDelete = (commentId) => {
    if (window.confirm('댓글을 삭제하시겠습니까?')) {
      fetch(`/api/comments/${commentId}`, { method: 'DELETE' })
        .then(() => setComments(comments.filter(c => c.comment_id !== commentId)));
    }
  };

  const handleCommentSubmit = (content) => {
    fetch(`/api/posts/${id}/comments`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ content }),
    })
      .then(res => res.json())
      .then(newComment => setComments([...comments, newComment]));
  };

  if (!post) return <div>Loading...</div>;

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h1>{post.title}</h1>
        <div>
          <Link to="/posts" className="btn btn-outline-secondary me-2">목록</Link>
          {/* Add edit button logic if user is author */}
          <button className="btn btn-outline-danger" onClick={handleDelete}>삭제</button>
        </div>
      </div>
      <div className="card mb-4">
        <div className="card-header">
          <div>
            <strong>작성자:</strong> {post.authorNickname || '익명'} &nbsp;
            <strong>작성일:</strong> {new Date(post.created_at).toLocaleString()} &nbsp;
            <strong>조회수:</strong> {post.view_count}
          </div>
        </div>
        <div className="card-body">
          <div className="post-content">{post.content}</div>
        </div>
      </div>
      {/* Comments */}
      <CommentForm onSubmit={handleCommentSubmit} />
      <CommentList comments={comments} onDelete={handleCommentDelete} currentUserId={null /* TODO: set user id */} />
    </div>
  );
};

export default PostDetailPage; 