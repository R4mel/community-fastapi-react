import axios from 'axios';

export const api = axios.create({
  baseURL: 'http://127.0.0.1:8000',  // localhost 대신 IP 주소 사용
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
  withCredentials: true,
  // Add request interceptor for debugging
  transformRequest: [
    (data, headers) => {
      console.log('Request Headers:', headers);
      console.log('Request Data:', data);
      
      // FormData는 그대로 전달
      if (data instanceof FormData) {
        return data;
      }
      
      return JSON.stringify(data);
    },
  ],
  // Add response interceptor for debugging
  transformResponse: [
    (data) => {
      console.log('Response Data:', data);
      try {
        return JSON.parse(data);
      } catch (e) {
        return data;
      }
    },
  ],
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers['Authorization'] = `Bearer ${token}`;
  }
  
  // FormData를 사용하는 경우 Content-Type 헤더 제거
  if (config.data instanceof FormData) {
    delete config.headers['Content-Type'];
  }
  
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // Handle specific error cases here if needed
      console.error('API Error:', error.response.data);
    }
    return Promise.reject(error);
  }
);

// User APIs
export const getUserProfile = async (userId) => {
  const response = await api.get(`/api/users/${userId}`);
  return response.data;
};

export const updateUserInfo = async (userId, userData) => {
  const response = await api.put(`/api/users/${userId}`, userData);
  return response.data;
};

// Category APIs
export const getCategories = async () => {
  try {
    const response = await api.get('/api/categories');
    console.log('Categories API response:', response); // 디버깅을 위한 로그
    return response.data;
  } catch (error) {
    console.error('Error fetching categories:', error);
    throw error;
  }
};

export const getCategory = async (categoryId) => {
  const response = await api.get(`/api/categories/${categoryId}`);
  return response.data;
};

// Post APIs
export const getPosts = async (params = {}) => {
  const response = await api.get('/api/posts', { params });
  return response.data;
};

export const getPost = async (postId) => {
  const response = await api.get(`/api/posts/${postId}`);
  return response.data;
};

export const createPost = async (postData) => {
  const response = await api.post('/api/posts', postData);
  return response.data;
};

export const updatePost = async (postId, postData) => {
  const response = await api.put(`/api/posts/${postId}`, postData);
  return response.data;
};

export const deletePost = async (postId) => {
  const response = await api.delete(`/api/posts/${postId}`);
  return response.data;
};

// Comment APIs
export const createComment = async (postId, commentData) => {
  const response = await api.post(`/api/posts/${postId}/comments`, commentData);
  return response.data;
};

export const getPostComments = async (postId) => {
  const response = await api.get(`/api/posts/${postId}/comments`);
  return response.data;
};

export const updateComment = async (commentId, commentData) => {
  const response = await api.put(`/api/comments/${commentId}`, commentData);
  return response.data;
};

export const deleteComment = async (postId, commentId) => {
  const response = await api.delete(`/api/posts/${postId}/comments/${commentId}`);
  return response.data;
};

// Kakao Auth APIs
export const getKakaoUrl = async () => {
  const response = await api.get('/api/auth/kakao/url');
  return response.data;
};

export const loginWithKakao = async (code) => {
  const response = await api.post('/api/auth/kakao', { code });
  return response.data;
};
