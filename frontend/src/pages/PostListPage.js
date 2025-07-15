import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../api/client';
import PostCard from '../components/PostCard';

const PostListPage = () => {
  const [posts, setPosts] = useState([]);
  const [keyword, setKeyword] = useState('');
  const [categoryId, setCategoryId] = useState(-1);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchPosts = async () => {
      try {
        setIsLoading(true);
        setError(null);
        const response = await api.get(`/api/posts?keyword=${encodeURIComponent(keyword)}&category_id=${categoryId}`);
        setPosts(response.data);
      } catch (error) {
        console.error('Error fetching posts:', error);
        setError('게시글을 불러오는데 실패했습니다.');
      } finally {
        setIsLoading(false);
      }
    };
    fetchPosts();
  }, [keyword, categoryId]);

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-800">게시판</h1>
      </div>
      
      <div className="mb-6">
        <input
          type="text"
          placeholder="게시글 검색..."
          value={keyword}
          onChange={(e) => setKeyword(e.target.value)}
          className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
        />
      </div>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg mb-6">
          {error}
        </div>
      )}

      {isLoading ? (
        <div className="flex justify-center py-10">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-blue-500"></div>
        </div>
      ) : (
        <div className="space-y-4">
          {posts.map(post => (
            <PostCard key={post.post_id} post={post} />
          ))}
          {posts.length === 0 && !error && (
            <div className="text-center py-10 text-gray-500">
              게시글이 없습니다.
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default PostListPage;