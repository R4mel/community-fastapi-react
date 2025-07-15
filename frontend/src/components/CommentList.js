import React from 'react';

const CommentList = ({ comments, onDelete, currentUserId }) => (
  <div className="space-y-4">
    <h3 className="text-lg font-semibold text-gray-900">댓글</h3>
    {comments.length === 0 ? (
      <p className="text-gray-500">아직 댓글이 없습니다.</p>
    ) : (
      comments.map(comment => (
        <div className="bg-white rounded-lg shadow p-4" key={comment.comment_id}>
          <div className="flex justify-between items-start">
            <div className="flex items-center">
              <img 
                src={comment.user?.profile_image || '/default-avatar.png'} 
                alt="프로필" 
                className="w-8 h-8 rounded-full mr-3"
              />
              <div>
                <div className="font-medium text-gray-900">
                  {comment.user?.nickname || '익명'}
                </div>
                <div className="text-sm text-gray-500">
                  {new Date(comment.created_at).toLocaleString('ko-KR', {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric',
                    hour: '2-digit',
                    minute: '2-digit'
                  })}
                </div>
              </div>
            </div>
            {currentUserId === comment.user_id && (
              <button
                className="text-sm text-red-600 hover:text-red-800 px-2 py-1 rounded hover:bg-red-50"
                onClick={() => onDelete(comment.comment_id)}
              >
                삭제
              </button>
            )}
          </div>
          <div className="mt-3 text-gray-700">{comment.content}</div>
        </div>
      ))
    )}
  </div>
);

export default CommentList;