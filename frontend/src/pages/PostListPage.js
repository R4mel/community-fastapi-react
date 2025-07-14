import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';

const PostListPage = () => {
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    fetch('/api/posts')
      .then(res => res.json())
      .then(setPosts);
  }, []);

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h1>게시판</h1>
        <Link to="/posts/new" className="btn btn-primary">글쓰기</Link>
      </div>
      <div className="card">
        <div className="card-body">
          <div className="table-responsive">
            <table className="table table-hover">
              <thead>
                <tr>
                  <th>번호</th>
                  <th>제목</th>
                  <th>작성자</th>
                  <th>작성일</th>
                  <th>조회수</th>
                </tr>
              </thead>
              <tbody>
                {posts.map((post, idx) => (
                  <tr key={post.post_id}>
                    <td>{posts.length - idx}</td>
                    <td>
                      <Link to={`/posts/${post.post_id}`} className="text-decoration-none fw-bold">
                        {post.title}
                      </Link>
                      <br />
                      <small className="text-muted">{post.categoryName || '카테고리'}</small>
                    </td>
                    <td>{post.authorNickname || '익명'}</td>
                    <td>{new Date(post.created_at).toLocaleDateString()}</td>
                    <td>{post.view_count || 0}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
      {posts.length === 0 && (
        <div className="text-center py-5">
          <h3 className="text-muted">아직 게시글이 없습니다</h3>
          <p className="text-muted">첫 번째 게시글을 작성해보세요!</p>
          <Link to="/posts/new" className="btn btn-primary">글쓰기</Link>
        </div>
      )}
    </div>
  );
};

export default PostListPage; 