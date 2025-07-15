import React, { useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { api } from '../api/client';

function KakaoCallback({ setUser }) {
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    const processKakaoLogin = async () => {
      console.log('KakaoCallback component mounted');
      
      try {
        const params = new URLSearchParams(location.search);
        const code = params.get('code');
        const error = params.get('error');

        console.log('Starting Kakao login process');
        console.log('Authorization code:', code);
        console.log('Current URL:', window.location.href);

        if (error) {
          console.error('Kakao auth error:', error);
          alert(`로그인 오류: ${error}`);
          navigate('/');
          return;
        }

        if (!code) {
          console.error('No authorization code received');
          alert('인증 코드를 받지 못했습니다.');
          navigate('/');
          return;
        }

        // Send authorization code to backend
        console.log('Sending authorization code to backend...');
        const requestData = { code: code };
        console.log('Request data:', requestData);

        const response = await api.post('/api/auth/kakao', requestData);
        console.log('Backend response:', response);
        
        if (response.data) {
          const { user, access_token } = response.data;
          console.log('Received user data:', user);
          console.log('Received access token:', access_token);
          
          if (access_token) {
            localStorage.setItem('access_token', access_token);
          }
          
          if (user) {
            localStorage.setItem('user', JSON.stringify(user));
            setUser(user);
          }
          
          alert('로그인 성공!');
          navigate('/');
        } else {
          console.error('Invalid response format:', response.data);
          throw new Error('서버로부터 올바른 응답을 받지 못했습니다.');
        }
      } catch (error) {
        console.error('Login process failed:', error);
        if (error.response) {
          console.error('Error response:', error.response.data);
          console.error('Error status:', error.response.status);
        }
        alert(`로그인 처리 중 오류가 발생했습니다: ${error.message}`);
        navigate('/');
      }
    };

    processKakaoLogin();
  }, [navigate, location, setUser]);

  return (
    <div className="flex justify-center items-center min-h-screen">
      <div className="text-center">
        <p className="text-lg mb-2">로그인 처리중...</p>
        <div className="w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mx-auto"></div>
      </div>
    </div>
  );
}

export default KakaoCallback;
