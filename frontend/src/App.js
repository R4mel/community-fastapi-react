import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import Layout from './components/Layout';
import HomePage from './pages/HomePage';
import PostListPage from './pages/PostListPage';
import PostDetailPage from './pages/PostDetailPage';
import PostFormPage from './pages/PostFormPage';

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/posts" element={<PostListPage />} />
          <Route path="/posts/new" element={<PostFormPage />} />
          <Route path="/posts/:id" element={<PostDetailPage />} />
          <Route path="/posts/:id/edit" element={<PostFormPage edit />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;
