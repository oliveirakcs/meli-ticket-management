// pages/Login.tsx

import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import mercadoLivreLogo from '../icons/mercado-livre.svg';
import '../styles/Login.css';

const Login: React.FC = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    const loginData = new URLSearchParams();
    loginData.append('grant_type', 'password');
    loginData.append('username', username);
    loginData.append('password', password);
    loginData.append('scope', '');
    loginData.append('client_id', 'string');
    loginData.append('client_secret', 'string');
    

    try {
      const response = await axios.post(
        'http://localhost:1201/api/v1/login/',
        loginData,
        {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
        }
      );

      const { access_token, role, scopes } = response.data;
      localStorage.setItem('access_token', access_token);
      localStorage.setItem('user_role', role);
      localStorage.setItem('user_scopes', JSON.stringify(scopes));

      navigate('/');
    } catch (error) {
      console.error('Erro ao fazer login:', error);
      alert('Credenciais inválidas');
    }
  };

  return (
    <div className="login">
      <div className="logo-container">
        <img src={mercadoLivreLogo} alt="Mercado Livre" className="logo" />
      </div>
      <h1>Login</h1>
      <form onSubmit={handleLogin}>
        <div>
          <label>Username:</label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Password:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit">Login</button>
      </form>
    </div>
  );
};

export default Login;
