import React from 'react';
import Navbar from './Navbar';

const Layout = ({ children, user, onLogout }) => (
  <>
    <Navbar user={user} onLogout={onLogout} />
    <div className="container main-content py-4">
      {children}
    </div>
  </>
);

export default Layout; 