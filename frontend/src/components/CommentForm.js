import React, { useState } from 'react';

const CommentForm = ({ onSubmit }) => {
  const [content, setContent] = useState('');
  const isLoggedIn = Boolean(localStorage.getItem('access_token'));

  if (!isLoggedIn) {
    return (
      <div className="bg-gray-50 rounded-lg p-4 text-center text-gray-500">
        댓글을 작성하려면 로그인이 필요합니다.
      </div>
    );
  }

  return (
    <form
      onSubmit={e => {
        e.preventDefault();
        if (content.trim()) {
          onSubmit(content);
          setContent('');
        }
      }}
      className="mb-4 bg-white rounded-lg shadow p-4"
    >
      <div className="mb-3">
        <label htmlFor="commentContent" className="block text-sm font-medium text-gray-700 mb-2">
          댓글 작성
        </label>
        <textarea
          id="commentContent"
          rows={3}
          value={content}
          onChange={e => setContent(e.target.value)}
          placeholder="댓글을 입력하세요..."
          required
          className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
        />
      </div>
      <div className="flex justify-end">
        <button
          type="submit"
          className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
        >
          댓글 작성
        </button>
      </div>
    </form>
  );
};

export default CommentForm; 