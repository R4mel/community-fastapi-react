import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import PostCard from '../components/PostCard';

const HomePage = () => {
  const [recentPosts, setRecentPosts] = useState([]);

  useEffect(() => {
    fetch('/api/posts')
      .then(res => res.json())
      .then(data => setRecentPosts(data.slice(0, 6)));
  }, []);

  return (
    <div className="container main-content py-4">
      {/* Welcome Section */}
      <div className="row mb-5">
        <div className="col-12">
          <div className="text-center">
            <div className="mt-4">
              <Link to="/posts/new" className="btn btn-primary btn-lg me-2">글쓰기</Link>
              <Link to="/posts" className="btn btn-outline-secondary btn-lg">게시판 보기</Link>
            </div>
          </div>
        </div>
      </div>
      {/* Recent Posts */}
      <div className="row">
        {recentPosts.map(post => (
          <div className="col-md-6 col-lg-4 mb-4" key={post.post_id}>
            <PostCard post={post} />
          </div>
        ))}
      </div>
    </div>
  );
};

export default HomePage; 