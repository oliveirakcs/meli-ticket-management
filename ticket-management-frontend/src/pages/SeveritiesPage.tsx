import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { fetchSeverities, createSeverity, updateSeverity, deleteSeverity } from '../services/api';
import { Severity, SeverityCreation } from '../types/generalTypes';
import SeverityModal from '../components/SeverityModal';
import mercadoLivreLogo from '../icons/mercado-livre.svg';

const SeveritiesPage: React.FC = () => {
  const [severities, setSeverities] = useState<Severity[]>([]);
  const [selectedSeverity, setSelectedSeverity] = useState<Severity | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isEditMode, setIsEditMode] = useState(false);
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const navigate = useNavigate();

  useEffect(() => {
    loadSeverities();
  }, []);

  const loadSeverities = async () => {
    try {
      const severitiesData = await fetchSeverities();
      setSeverities(severitiesData);
    } catch (error) {
      console.error('Erro ao buscar Severities:', error);
      alert('Erro ao carregar Severities.');
    }
  };

  const handleCreateSeverity = async (severity: SeverityCreation) => {
    try {
      const newSeverity = await createSeverity(severity);
      setSeverities((prevSeverities) => [...prevSeverities, newSeverity]);
      alert('Severidade criada com sucesso!');
    } catch (error) {
      console.error('Erro ao criar severidade:', error);
      alert('Erro ao criar severidade.');
    }
  };

  const handleUpdateSeverity = async (updatedSeverity: Severity) => {
    try {
      await updateSeverity(updatedSeverity.id, updatedSeverity);
      setSeverities((prevSeverities) =>
        prevSeverities.map((severity) => (severity.id === updatedSeverity.id ? updatedSeverity : severity))
      );
      alert('Severidade atualizada com sucesso!');
    } catch (error) {
      console.error('Erro ao atualizar severidade:', error);
      alert('Erro ao atualizar severidade.');
    }
  };

  const handleDeleteSeverity = async (id: string) => {
    const confirmDelete = window.confirm(
      'Tem certeza que deseja deletar esta Severity?'
    );
    if (confirmDelete) {
    try {
      await deleteSeverity(id);
      setSeverities((prevSeverities) => prevSeverities.filter((severity) => severity.id !== id));
      alert('Severidade deletada com sucesso!');
    } catch (error) {
      console.error('Erro ao deletar severidade:', error);
      alert('Erro ao deletar severidade.');
    }
  }
};

  const handleEditClick = (severity: Severity) => {
    setSelectedSeverity(severity);
    setIsEditMode(true);
    setIsModalOpen(true);
  };

  const handleCreateClick = () => {
    setSelectedSeverity(null);
    setIsEditMode(false);
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
    setSelectedSeverity(null);
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
                      borderRadius: '4px',
                      cursor: 'pointer',
                      transition: 'background-color 0.3s',
                      backgroundColor: '#0056b3',
                      color: 'white',
                    }}
                    onClick={() => navigate('/users')}
                    onMouseEnter={(e) =>
                      ((e.target as HTMLElement).style.backgroundColor =
                        '#004494')
                    }
                    onMouseLeave={(e) =>
                      ((e.target as HTMLElement).style.backgroundColor =
                        '#0056b3')
                    }
                  >
                    Usuários
                  </li>
                </ul>
              </div>
            )}
          </div>
          <div
            style={{
              flex: 1,
            }}
          ></div>
        </div>

        <h1
          style={{
            textAlign: 'center',
            color: '#333',
          }}
        >
          Severities Cadastradas
        </h1>

        <button
          onClick={handleCreateClick}
          style={{
            backgroundColor: '#007bff',
            color: 'white',
            padding: '10px 20px',
            borderRadius: '5px',
            border: 'none',
            cursor: 'pointer',
            marginBottom: '20px',
            display: 'block',
            marginLeft: 'auto',
            transition: 'background-color 0.3s ease',
          }}
          onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = '#0056b3')}
          onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = '#007bff')}
        >
          Criar Nova Severidade
        </button>

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
                Nível
              </th>
              <th style={{ padding: '10px', borderBottom: '2px solid #ddd' }}>
                Descrição
              </th>
              <th style={{ padding: '10px', borderBottom: '2px solid #ddd' }}>
                Ações
              </th>
            </tr>
          </thead>
          <tbody>
            {severities.map((severity) => (
              <tr
                key={severity.id}
                style={{
                  backgroundColor: '#fff',
                  borderBottom: '1px solid #ddd',
                }}
              >
                <td style={{ padding: '10px', textAlign: 'center' }}>
                  {severity.level}
                </td>
                <td style={{ padding: '10px', textAlign: 'center' }}>
                  {severity.description}
                </td>
                <td style={{ padding: '10px', textAlign: 'center' }}>
                  <button
                    onClick={() => handleEditClick(severity)}
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
                    onClick={() => handleDeleteSeverity(severity.id)}
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
          <SeverityModal
            severity={selectedSeverity}
            isEditMode={isEditMode}
            onClose={closeModal}
            onSubmit={(severity) => {
              if (isEditMode) {
                handleUpdateSeverity(severity as Severity);
              } else {
                handleCreateSeverity(severity as SeverityCreation);
              }
            }}
          />
        )}
      </div>
    </div>
  );
};

export default SeveritiesPage;
