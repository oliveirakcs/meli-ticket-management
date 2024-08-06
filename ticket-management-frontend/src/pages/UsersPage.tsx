import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { fetchUsers, createUser, updateUser, deleteUser, createRandomUser } from '../services/api'; // Importe a função
import { User, UserCreation } from '../types/generalTypes';
import UserModal from '../components/UserModal';
import mercadoLivreLogo from '../icons/mercado-livre.svg';

const UsersPage: React.FC = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [selectedUser, setSelectedUser] = useState<User | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isEditMode, setIsEditMode] = useState(false);
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const navigate = useNavigate();

  useEffect(() => {
    loadUsers();
  }, []);

  const loadUsers = async () => {
    try {
      const usersData = await fetchUsers();
      setUsers(usersData);
    } catch (error) {
      console.error('Erro ao buscar usuários:', error);
      alert('Erro ao carregar usuários.');
    }
  };

  const handleCreateUser = async (user: UserCreation) => {
    try {
      const newUser = await createUser(user);
      setUsers((prevUsers) => [...prevUsers, newUser]);
      alert('Usuário criado com sucesso!');
    } catch (error) {
      console.error('Erro ao criar usuário:', error);
      alert('Erro ao criar usuário.');
    }
  };

  const handleUpdateUser = async (updatedUser: User) => {
    try {
      await updateUser(updatedUser.id, updatedUser);
      setUsers((prevUsers) =>
        prevUsers.map((user) => (user.id === updatedUser.id ? updatedUser : user))
      );
      alert('Usuário atualizado com sucesso!');
    } catch (error) {
      console.error('Erro ao atualizar usuário:', error);
      alert('Erro ao atualizar usuário.');
    }
  };

  const handleDeleteUser = async (id: string) => {
    const confirmDelete = window.confirm(
      'Tem certeza que deseja deletar este Usuário?'
    );
    if (confirmDelete) {
      try {
        await deleteUser(id);
        setUsers((prevUsers) => prevUsers.filter((user) => user.id !== id));
        alert('Usuário deletado com sucesso!');
      } catch (error) {
        console.error('Erro ao deletar usuário:', error);
        alert('Erro ao deletar usuário.');
      }
    }
  };

  const handleEditClick = (user: User) => {
    setSelectedUser(user);
    setIsEditMode(true);
    setIsModalOpen(true);
  };

  const handleCreateClick = () => {
    setSelectedUser(null);
    setIsEditMode(false);
    setIsModalOpen(true);
  };

  const handleCreateRandomUser = async () => {
    try {
      const newUser = await createRandomUser(); // Chama a função para criar usuário aleatório
      setUsers((prevUsers) => [...prevUsers, newUser]);
      alert('Usuário aleatório criado com sucesso!');
    } catch (error) {
      console.error('Erro ao criar usuário aleatório:', error);
      alert('Erro ao criar usuário aleatório.');
    }
  };

  const closeModal = () => {
    setIsModalOpen(false);
    setSelectedUser(null);
  };

  const toggleMenu = () => {
    setIsMenuOpen((prev) => !prev);
  };

  return (
    <div
      style={{
        maxWidth: '1200px',
        margin: '0 auto',
        padding: '20px',
      }}
    >
      <div
        style={{
          marginBottom: '20px',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          flexDirection: 'column',
          width: '100%',
          marginTop: '10px',
        }}
      >
        <img
          src={mercadoLivreLogo}
          alt="Mercado Livre"
          style={{
            width: '150px',
            height: 'auto',
          }}
        />
        <span
          style={{
            color: '#2d3277',
            fontSize: '18px',
            fontFamily: 'Arial, sans-serif',
            marginTop: '10px',
            textAlign: 'center',
          }}
        >
          Ticket Management App
        </span>
      </div>
      
      <div
        style={{
          padding: '20px',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          marginTop: '20px',
          position: 'relative',
        }}
      >
        
        <div
          style={{
            display: 'flex',
            justifyContent: 'space-between',
            width: '100%',
          }}
        >
          
          <div>
            <button
              style={{
                backgroundColor: isMenuOpen ? '#0056b3' : '#007bff',
                border: 'none',
                width: '60px',
                height: '50px',
                borderRadius: '5px',
                color: 'white',
                cursor: 'pointer',
                transition: 'transform 0.3s ease, background-color 0.3s ease',
                transform: isMenuOpen ? 'rotate(90deg)' : 'rotate(0deg)',
                fontSize: '24px',
                boxShadow: '0 2px 4px rgba(0, 0, 0, 0.2)',
                outline: 'none',
                position: 'relative',
                marginBottom: '10px',
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'center',
                alignItems: 'center',
              }}
              onClick={toggleMenu}
              onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = '#0056b3')}
              onMouseLeave={(e) =>
                (e.currentTarget.style.backgroundColor = isMenuOpen ? '#0056b3' : '#007bff')
              }
            >
              <span
                style={{
                  display: 'block',
                  width: '25px',
                  height: '3px',
                  backgroundColor: 'white',
                  margin: '2px auto',
                  transition: 'all 0.3s',
                  transform: isMenuOpen ? 'rotate(-45deg) translate(-5px, 5px)' : 'rotate(0)',
                }}
              />
              <span
                style={{
                  display: 'block',
                  width: '25px',
                  height: '3px',
                  backgroundColor: 'white',
                  margin: '2px auto',
                  transition: 'all 0.3s',
                  opacity: isMenuOpen ? 0 : 1,
                }}
              />
              <span
                style={{
                  display: 'block',
                  width: '25px',
                  height: '3px',
                  backgroundColor: 'white',
                  margin: '2px auto',
                  transition: 'all 0.3s',
                  transform: isMenuOpen ? 'rotate(45deg) translate(-5px, -5px)' : 'rotate(0)',
                }}
              />
            </button>
            {isMenuOpen && (
              <div
                style={{
                  position: 'absolute',
                  backgroundColor: '#007bff',
                  padding: '20px',
                  marginTop: '10px',
                  borderRadius: '8px',
                  boxShadow: '0 4px 8px rgba(0, 0, 0, 0.2)',
                  zIndex: 1000,
                }}
              >
                <ul style={{ listStyleType: 'none', padding: 0, margin: 0 }}>
                  <li
                    style={{
                      padding: '10px',
                      marginBottom: '5px',
                      borderRadius: '4px',
                      cursor: 'pointer',
                      transition: 'background-color 0.3s',
                      backgroundColor: '#0056b3',
                      color: 'white',
                    }}
                    onClick={() => navigate('/')}
                    onMouseEnter={(e) =>
                      ((e.target as HTMLElement).style.backgroundColor =
                        '#004494')
                    }
                    onMouseLeave={(e) =>
                      ((e.target as HTMLElement).style.backgroundColor =
                        '#0056b3')
                    }
                  >
                    Página Principal
                  </li>
                  <li
                    style={{
                      padding: '10px',
                      marginBottom: '5px',
                      borderRadius: '4px',
                      cursor: 'pointer',
                      transition: 'background-color 0.3s',
                      backgroundColor: '#0056b3',
                      color: 'white',
                    }}
                    onClick={() => navigate('/categories')}
                    onMouseEnter={(e) =>
                      ((e.target as HTMLElement).style.backgroundColor =
                        '#004494')
                    }
                    onMouseLeave={(e) =>
                      ((e.target as HTMLElement).style.backgroundColor =
                        '#0056b3')
                    }
                  >
                    Categorias
                  </li>
                  <li
                    style={{
                      padding: '10px',
                      marginBottom: '5px',
                      borderRadius: '4px',
                      cursor: 'pointer',
                      transition: 'background-color 0.3s',
                      backgroundColor: '#0056b3',
                      color: 'white',
                    }}
                    onClick={() => navigate('/severities')}
                    onMouseEnter={(e) =>
                      ((e.target as HTMLElement).style.backgroundColor =
                        '#004494')
                    }
                    onMouseLeave={(e) =>
                      ((e.target as HTMLElement).style.backgroundColor =
                        '#0056b3')
                    }
                  >
                    Severities
                  </li>
                </ul>
              </div>
            )}
          </div>
          <div
            style={{
              flex: 1,
            }}
          >
          </div>
          
        </div>

        <h1
          style={{
            textAlign: 'center',
            color: '#333',
          }}
        >
          Usuários
        </h1>

        {/* Botões de criação de usuários */}
        <div
          style={{
            display: 'flex',
            justifyContent: 'flex-end',
            width: '100%',
            marginBottom: '20px',
          }}
        >
          <button
            onClick={handleCreateClick}
            style={{
              backgroundColor: '#007bff',
              color: 'white',
              padding: '10px 20px',
              borderRadius: '5px',
              border: 'none',
              cursor: 'pointer',
              transition: 'background-color 0.3s ease',
              marginRight: '10px', // Espaço entre os botões
            }}
            onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = '#0056b3')}
            onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = '#007bff')}
          >
            Criar Novo Usuário
          </button>

          <button
            onClick={handleCreateRandomUser}
            style={{
              backgroundColor: '#28a745',
              color: 'white',
              padding: '10px 20px',
              borderRadius: '5px',
              border: 'none',
              cursor: 'pointer',
              transition: 'background-color 0.3s ease',
            }}
            onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = '#218838')}
            onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = '#28a745')}
          >
            Criar Novo Usuário Randomico
          </button>
        </div>

        <table
          style={{
            width: '100%',
            borderCollapse: 'collapse',
            boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)',
            marginTop: '20px',
          }}
        >
          <thead>
            <tr
              style={{
                backgroundColor: '#f4f4f4',
                color: '#333',
              }}
            >
              <th style={{ padding: '10px', borderBottom: '2px solid #ddd' }}>
                Nome
              </th>
              <th style={{ padding: '10px', borderBottom: '2px solid #ddd' }}>
                Username
              </th>
              <th style={{ padding: '10px', borderBottom: '2px solid #ddd' }}>
                Email
              </th>
              <th style={{ padding: '10px', borderBottom: '2px solid #ddd' }}>
                Role
              </th>
              <th style={{ padding: '10px', borderBottom: '2px solid #ddd' }}>
                Ações
              </th>
            </tr>
          </thead>
          <tbody>
            {users.map((user) => (
              <tr
                key={user.id}
                style={{
                  backgroundColor: '#fff',
                  borderBottom: '1px solid #ddd',
                }}
              >
                <td style={{ padding: '10px', textAlign: 'center' }}>
                  {user.name}
                </td>
                <td style={{ padding: '10px', textAlign: 'center' }}>
                  {user.username}
                </td>
                <td style={{ padding: '10px', textAlign: 'center' }}>
                  {user.email}
                </td>
                <td style={{ padding: '10px', textAlign: 'center' }}>
                  {user.role}
                </td>
                <td style={{ padding: '10px', textAlign: 'center' }}>
                  <button
                    onClick={() => handleEditClick(user)}
                    style={{
                      backgroundColor: '#ffc107',
                      color: '#333',
                      padding: '5px 10px',
                      borderRadius: '5px',
                      border: 'none',
                      cursor: 'pointer',
                      marginRight: '5px',
                      transition: 'background-color 0.3s ease',
                    }}
                    onMouseEnter={(e) =>
                      (e.currentTarget.style.backgroundColor = '#e0a800')
                    }
                    onMouseLeave={(e) =>
                      (e.currentTarget.style.backgroundColor = '#ffc107')
                    }
                  >
                    Editar
                  </button>
                  <button
                    onClick={() => handleDeleteUser(user.id)}
                    style={{
                      backgroundColor: '#dc3545',
                      color: 'white',
                      padding: '5px 10px',
                      borderRadius: '5px',
                      border: 'none',
                      cursor: 'pointer',
                      transition: 'background-color 0.3s ease',
                    }}
                    onMouseEnter={(e) =>
                      (e.currentTarget.style.backgroundColor = '#c82333')
                    }
                    onMouseLeave={(e) =>
                      (e.currentTarget.style.backgroundColor = '#dc3545')
                    }
                  >
                    Deletar
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>

        {isModalOpen && (
          <UserModal
            user={selectedUser}
            isEditMode={isEditMode}
            onClose={closeModal}
            onSubmit={(user) => {
              if (isEditMode) {
                handleUpdateUser(user as User);
              } else {
                handleCreateUser(user as UserCreation);
              }
            }}
          />
        )}
      </div>
    </div>
  );
};

export default UsersPage;
