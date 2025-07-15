import React from 'react';
import { Outlet } from 'react-router-dom';
import Navbar from './Navbar';
import { Helmet } from 'react-helmet';

const Layout = ({ user, onLogout, title }) => {
  const pageTitle = title ? `${title} - 커뮤니티` : '커뮤니티';
  
  const confirmDelete = (message) => {
    return window.confirm(message || '정말 삭제하시겠습니까?');
  };

  // Add confirmDelete to window object for global access
  React.useEffect(() => {
    window.confirmDelete = confirmDelete;
  }, []);

  return (
    <>
      <Helmet>
        <title>{pageTitle}</title>
      </Helmet>
      
      <Navbar user={user} onLogout={onLogout} />
      
      <main className="container mx-auto px-4 py-8">
        <Outlet />
      </main>
    </>
  );
};

export default Layout; 