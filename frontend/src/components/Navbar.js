import React from 'react';    
import { Link } from 'react-router-dom';

function Navbar({ user, onLogout }) {
  const handleKakaoLogin = () => {
    const clientId = '1dfa467a82b419968b0ec0b32f7389d4';
    const redirectUri = encodeURIComponent('http://localhost:3000/oauth/callback/kakao');
    
    const params = {
      client_id: clientId,
      redirect_uri: 'http://localhost:3000/oauth/callback/kakao',
      response_type: 'code'
    };
    
    const queryString = Object.entries(params)
      .map(([key, value]) => `${key}=${encodeURIComponent(value)}`)
      .join('&');
    
    const KAKAO_AUTH_URL = `https://kauth.kakao.com/oauth/authorize?${queryString}`;
    console.log('Redirecting to:', KAKAO_AUTH_URL);
    
    window.location.href = KAKAO_AUTH_URL;
  };

  return (
    <nav className="bg-gray-800 p-4">
      <div className="container mx-auto flex justify-between items-center">
        <Link to="/" className="text-white font-bold text-xl">
          Community
        </Link>
        <div className="flex items-center space-x-4">
          {user ? (
            <>
              <Link to="/posts/new" className="text-gray-300 hover:text-white">
                글쓰기
              </Link>
              <div className="flex items-center space-x-2">
                {user.profile_image && (
                  <img
                    src={user.profile_image}
                    alt="Profile"
                    className="w-8 h-8 rounded-full"
                  />
                )}
                <span className="text-gray-300">{user.nickname}</span>
                <button
                  onClick={onLogout}
                  className="bg-red-600 text-white px-3 py-1 rounded hover:bg-red-700"
                >
                  로그아웃
                </button>
              </div>
            </>
          ) : (
            <button
              onClick={handleKakaoLogin}
              className="bg-yellow-400 text-black px-4 py-2 rounded hover:bg-yellow-500"
            >
              카카오 로그인
            </button>
          )}
        </div>
      </div>
    </nav>
  );
}

export default Navbar;