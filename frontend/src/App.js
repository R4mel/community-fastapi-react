import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import HomePage from './pages/HomePage';
import PostListPage from './pages/PostListPage';
import PostDetailPage from './pages/PostDetailPage';
import PostFormPage from './pages/PostFormPage';
import KakaoCallback from './pages/KakaoCallback';
import './App.css';

function App() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    // Load user from localStorage on app start
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    }
  }, []);

  // Function to handle logout
  const handleLogout = () => {
    localStorage.removeItem('user');
    setUser(null);
  };

  return (
    <Router>
      <Routes>
        <Route element={<Layout user={user} onLogout={handleLogout} />}>
          <Route path="/" element={<PostListPage />} />
          <Route path="/posts" element={<PostListPage />} />
          <Route path="/posts/new" element={user ? <PostFormPage /> : <PostListPage />} />
          <Route path="/posts/:id" element={<PostDetailPage />} />
          <Route path="/oauth/callback/kakao" element={<KakaoCallback setUser={setUser} />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;
