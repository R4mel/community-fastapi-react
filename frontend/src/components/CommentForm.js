import React, { useState } from 'react';

const CommentForm = ({ onSubmit }) => {
  const [content, setContent] = useState('');
  return (
    <form
      onSubmit={e => {
        e.preventDefault();
        if (content.trim()) {
          onSubmit(content);
          setContent('');
        }
      }}
      className="mb-4"
    >
      <div className="mb-3">
        <label htmlFor="commentContent" className="form-label">댓글 작성</label>
        <textarea
          id="commentContent"
          className="form-control"
          rows={3}
          value={content}
          onChange={e => setContent(e.target.value)}
          placeholder="댓글을 입력하세요..."
          required
        />
      </div>
      <button type="submit" className="btn btn-primary">댓글 작성</button>
    </form>
  );
};

export default CommentForm; 