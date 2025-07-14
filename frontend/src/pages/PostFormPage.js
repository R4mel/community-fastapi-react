import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';

const PostFormPage = ({ edit }) => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [post, setPost] = useState({ title: '', content: '', category_id: '' });

  useEffect(() => {
    if (edit && id) {
      fetch(`/api/posts/${id}`)
        .then(res => res.json())
        .then(setPost);
    }
  }, [edit, id]);

  const handleChange = e => {
    setPost({ ...post, [e.target.name]: e.target.value });
  };

  const handleSubmit = e => {
    e.preventDefault();
    const method = edit ? 'PUT' : 'POST';
    const url = edit ? `/api/posts/${id}` : '/api/posts';
    fetch(url, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(post),
    })
      .then(() => navigate('/posts'));
  };

  return (
    <div>
      <h1>{edit ? '게시글 수정' : '글쓰기'}</h1>
      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <label className="form-label">제목</label>
          <input type="text" className="form-control" name="title" value={post.title} onChange={handleChange} required />
        </div>
        <div className="mb-3">
          <label className="form-label">카테고리</label>
          <input type="text" className="form-control" name="category_id" value={post.category_id} onChange={handleChange} required />
        </div>
        <div className="mb-3">
          <label className="form-label">내용</label>
          <textarea className="form-control" name="content" rows={10} value={post.content} onChange={handleChange} required />
        </div>
        <div className="d-flex justify-content-end gap-2">
          <button type="button" className="btn btn-outline-secondary" onClick={() => navigate('/posts')}>취소</button>
          <button type="submit" className="btn btn-primary">{edit ? '수정 완료' : '글쓰기'}</button>
        </div>
      </form>
    </div>
  );
};

export default PostFormPage; 