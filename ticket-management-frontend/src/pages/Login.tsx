import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { login } from '../services/api'; // Importando a função de login
import mercadoLivreLogo from '../icons/mercado-livre.svg';

const Login: React.FC = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    try {
      const { access_token, role, scopes } = await login(username, password);
      
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
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        height: '100vh',
        backgroundColor: '#f4f4f4',
      }}
    >
      <div style={{ marginBottom: '20px' }}>
        <img
          src={mercadoLivreLogo}
          alt="Mercado Livre"
          style={{ width: '150px', height: 'auto' }}
        />
      </div>
      <h1 style={{ marginBottom: '20px', color: '#333' }}>Login</h1>
      <form
        onSubmit={handleLogin}
        style={{
          backgroundColor: '#fff',
          padding: '40px',
          borderRadius: '5px',
          boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)',
          width: '100%',
          maxWidth: '400px',
        }}
      >
        <div style={{ marginBottom: '20px' }}>
          <label
            style={{
              display: 'block',
              fontWeight: 'bold',
              marginBottom: '8px',
              color: '#333',
            }}
          >
            Username:
          </label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
            style={{
              width: '100%',
              padding: '8px',
              borderRadius: '4px',
              border: '1px solid #ccc',
              boxSizing: 'border-box',
            }}
          />
        </div>
        <div style={{ marginBottom: '20px' }}>
          <label
            style={{
              display: 'block',
              fontWeight: 'bold',
              marginBottom: '8px',
              color: '#333',
            }}
          >
            Password:
          </label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            style={{
              width: '100%',
              padding: '8px',
              borderRadius: '4px',
              border: '1px solid #ccc',
              boxSizing: 'border-box',
            }}
          />
        </div>
        <button
          type="submit"
          style={{
            width: '100%',
            padding: '12px',
            fontSize: '16px',
            backgroundColor: '#007bff',
            color: 'white',
            border: 'none',
            borderRadius: '5px',
            cursor: 'pointer',
            transition: 'background-color 0.3s ease',
          }}
          onMouseEnter={(e) =>
            (e.currentTarget.style.backgroundColor = '#0056b3')
          }
          onMouseLeave={(e) =>
            (e.currentTarget.style.backgroundColor = '#007bff')
          }
        >
          Login
        </button>
      </form>
    </div>
  );
};

export default Login;
