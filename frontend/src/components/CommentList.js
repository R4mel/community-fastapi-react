import React from 'react';

const CommentList = ({ comments, onDelete, currentUserId }) => (
  <div>
    <h3>댓글</h3>
    {comments.length === 0 ? (
      <p className="text-muted">아직 댓글이 없습니다.</p>
    ) : (
      comments.map(comment => (
        <div className="comment-item mb-3" key={comment.comment_id}>
          <div className="d-flex justify-content-between align-items-start">
            <div>
              <strong>{comment.authorNickname || '익명'}</strong>
              <small className="text-muted ms-2">{new Date(comment.created_at).toLocaleString()}</small>
            </div>
            {currentUserId === comment.user_id && (
              <button
                className="btn btn-sm btn-outline-danger"
                onClick={() => onDelete(comment.comment_id)}
              >
                삭제
              </button>
            )}
          </div>
          <div className="mt-2">{comment.content}</div>
        </div>
      ))
    )}
  </div>
);

export default CommentList; 