import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = ({ user, onLogout }) => (
  <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
    <div className="container">
      <Link className="navbar-brand" to="/">커뮤니티</Link>
      <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
        <span className="navbar-toggler-icon"></span>
      </button>
      <div className="collapse navbar-collapse" id="navbarNav">
        <ul className="navbar-nav me-auto">
          <li className="nav-item">
            <Link className="nav-link" to="/">홈</Link>
          </li>
          <li className="nav-item">
            <Link className="nav-link" to="/posts">게시판</Link>
          </li>
        </ul>
        <ul className="navbar-nav">
          {!user ? (
            <li className="nav-item">
              <a className="nav-link" href="/oauth2/authorization/kakao">
                <img src="/kakao_login_medium_narrow.png" alt="카카오 로그인" style={{ height: 20 }} />
              </a>
            </li>
          ) : (
            <>
              <span className="navbar-text me-3">{user.nickname || '사용자'}</span>
              <button className="nav-link btn btn-link" onClick={onLogout}>로그아웃</button>
            </>
          )}
        </ul>
      </div>
    </div>
  </nav>
);

export default Navbar; 