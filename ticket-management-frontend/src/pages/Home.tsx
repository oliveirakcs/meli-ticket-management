import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { fetchTickets, deleteTicket, generateComment } from '../services/api';
import CreateTicketModal from '../components/CreateTicketModal';
import EditTicketModal from '../components/EditTicketModal';
import { capitalizeWords } from '../utils/utils';
import mercadoLivreLogo from '../icons/mercado-livre.svg';
interface Category {
  id: string;
  name: string;
  subcategories: Subcategory[];
}

interface Subcategory {
  id: string;
  name: string;
  category_id: string;
}

interface Severity {
  id: string;
  level: number;
  description: string;
}

export interface Ticket {
  id: string;
  title: string;
  description: string;
  categories: Category[];
  severity: Severity;
  status: string;
  comment: string;
  comment_user: string;
  created_at: string;
  updated_at: string;
}

const severityColors: { [key: number]: string } = {
  4: '#248c3c',
  3: '#a67e07',
  2: '#dc3545',
};

const Home: React.FC = () => {
  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [selectedTicket, setSelectedTicket] = useState<Ticket | null>(null);
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const navigate = useNavigate();
  const detailsRef = useRef<HTMLDivElement>(null);
  const userScopes = JSON.parse(localStorage.getItem('user_scopes') || '[]');

  useEffect(() => {
    const loadTickets = async () => {
      try {
        const ticketData = await fetchTickets();
        
        ticketData.sort((a: Ticket, b: Ticket) => {
          if (b.severity.level !== a.severity.level) {
            return b.severity.level - a.severity.level;
          }
          return new Date(b.created_at).getTime() - new Date(a.created_at).getTime();
        });
        
        setTickets(ticketData);
      } catch (error) {
        console.error('Erro ao buscar tickets:', error);
      }
    };

    loadTickets();
  }, []);

  useEffect(() => {
    const handleEscKey = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        setSelectedTicket(null);
        setIsEditModalOpen(false);
      }
    };

    const handleClickOutside = (event: MouseEvent) => {
      if (
        detailsRef.current &&
        !detailsRef.current.contains(event.target as Node)
      ) {
        setSelectedTicket(null);
        setIsEditModalOpen(false);
      }
    };

    document.addEventListener('keydown', handleEscKey);
    document.addEventListener('mousedown', handleClickOutside);

    return () => {
      document.removeEventListener('keydown', handleEscKey);
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  const handleCardClick = (ticket: Ticket) => {
    setSelectedTicket(ticket);
  };

  const handleEdit = (id: string) => {
    const ticketToEdit = tickets.find((ticket) => ticket.id === id);
    if (ticketToEdit) {
      setSelectedTicket(ticketToEdit);
      setIsEditModalOpen(true);
    }
  };

  const handleDelete = async (id: string) => {
    const confirmDelete = window.confirm(
      'Tem certeza que deseja deletar este ticket?'
    );
    if (confirmDelete) {
      try {
        await deleteTicket(id);
        setTickets((prevTickets) =>
          prevTickets.filter((ticket) => ticket.id !== id)
        );
        setSelectedTicket(null);
        alert('Ticket deletado com sucesso!');
      } catch (error) {
        console.error('Erro ao deletar ticket:', error);
        alert('Erro ao deletar ticket.');
      }
    }
  };

  const handleGenerateComment = async (id: string) => {
    try {
      const { comment, comment_user } = await generateComment(id);
      const updatedTicket = {
        ...selectedTicket!,
        comment,
        comment_user,
      };
      setSelectedTicket(updatedTicket);

      setTickets((prevTickets) =>
        prevTickets.map((ticket) =>
          ticket.id === updatedTicket.id ? updatedTicket : ticket
        )
      );

      alert('Comentário gerado com sucesso!');
    } catch (error) {
      console.error('Erro ao gerar comentário:', error);
      alert('Erro ao gerar comentário.');
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user_role');
    localStorage.removeItem('user_scopes');
    navigate('/login');
  };

  const handleCreateTicket = () => {
    setIsCreateModalOpen(true);
  };

  const handleCloseCreateModal = () => {
    setIsCreateModalOpen(false);
  };

  const handleCloseEditModal = () => {
    setIsEditModalOpen(false);
  };

  const handleTicketCreated = async () => {
    setIsCreateModalOpen(false);
    const ticketData = await fetchTickets();
    
    ticketData.sort((a: Ticket, b: Ticket) => {
      if (b.severity.level !== a.severity.level) {
        return b.severity.level - a.severity.level;
      }
      return new Date(b.created_at).getTime() - new Date(a.created_at).getTime();
    });
    
    setTickets(ticketData);
  };

  const handleTicketUpdated = async (updatedTicket: Ticket) => {
    setTickets((prevTickets) =>
      prevTickets.map((ticket) =>
        ticket.id === updatedTicket.id ? updatedTicket : ticket
      )
    );
    setSelectedTicket(updatedTicket);
    setIsEditModalOpen(false);
  };

  const handleNavigation = (path: string) => {
    navigate(path);
    setIsMenuOpen(false);
  };

  const handleCardClickEnhanced = (ticket: Ticket) => {
    if (selectedTicket && selectedTicket.id === ticket.id) {
    }
    handleCardClick(ticket);
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
          justifyContent: 'space-between',
          alignItems: 'center',
          width: '100%',
          marginTop: '10px',
        }}
      >
        <div
          style={{
            flex: 1,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            paddingLeft: '80px',
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
              fontSize: '24px',
              fontFamily: 'Arial, sans-serif',
              marginTop: '10px',
              textAlign: 'center',
            }}
          >
            Ticket Management App
          </span>
        </div>
        <button
          onClick={handleLogout}
          style={{
            backgroundColor: '#f44336',
            color: 'white',
            padding: '10px 20px',
            borderRadius: '5px',
            border: 'none',
            cursor: 'pointer',
            transition: 'background-color 0.3s ease',
            marginLeft: 'auto', // Push the button to the right
          }}
          onMouseEnter={(e) =>
            (e.currentTarget.style.backgroundColor = '#d32f2f')
          }
          onMouseLeave={(e) =>
            (e.currentTarget.style.backgroundColor = '#f44336')
          }
        >
          Logout
        </button>
      </div>


      
      <div
        style={{
          padding: '10px',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          marginTop: '5px',
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
          {userScopes.includes('admin') && (
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
                onClick={() => setIsMenuOpen((prev) => !prev)}
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
                      onClick={() => handleNavigation('/categories')}
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
                      onClick={() => handleNavigation('/severities')}
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
                    <li
                      style={{
                        padding: '10px',
                        borderRadius: '4px',
                        cursor: 'pointer',
                        transition: 'background-color 0.3s',
                        backgroundColor: '#0056b3',
                        color: 'white',
                      }}
                      onClick={() => handleNavigation('/users')}
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
          )}
          <div
            style={{
              flex: 1,
            }}
          ></div>
          
        </div>

        <h1 style={{ color: '#333', textAlign: 'center' }}>Tickets</h1>

        <button
          onClick={handleCreateTicket}
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
          onMouseEnter={(e) =>
            (e.currentTarget.style.backgroundColor = '#0056b3')
          }
          onMouseLeave={(e) =>
            (e.currentTarget.style.backgroundColor = '#007bff')
          }
        >
          Criar Ticket
        </button>

        <div
          style={{
            display: 'flex',
            flexWrap: 'wrap',
            gap: '20px',
            justifyContent: 'center',
            maxWidth: '1000px',
          }}
        >
          {tickets.map((ticket) => (
            <div
              key={ticket.id}
              onClick={() => handleCardClickEnhanced(ticket)}
              style={{
                border: `2px solid ${severityColors[ticket.severity.level]}`,
                backgroundColor: '#fff',
                borderRadius: '5px',
                boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)',
                padding: '15px',
                width: '250px',
                cursor: 'pointer',
                transition: 'transform 0.3s ease',
              }}
              onMouseEnter={(e) =>
                (e.currentTarget.style.transform = 'translateY(-5px)')
              }
              onMouseLeave={(e) =>
                (e.currentTarget.style.transform = 'translateY(0)')
              }
            >
              <h2
                style={{
                  margin: '0',
                  color: '#555',
                  fontSize: '1.2em',
                }}
              >
                {ticket.title}
              </h2>
              <p
                style={{
                  margin: '5px 0',
                  color: '#777',
                }}
              >
                Severity:{' '}
                <span
                  style={{
                    color: severityColors[ticket.severity.level],
                  }}
                >
                  {ticket.severity.description}
                </span>
              </p>
              <p
                style={{
                  margin: '5px 0',
                  color: '#777',
                }}
              >
                Criado em: {new Date(ticket.created_at).toLocaleString()}
              </p>
              <p
                style={{
                  margin: '5px 0',
                  color: '#777',
                }}
              >
                Status: {capitalizeWords(ticket.status)}
              </p>
            </div>
          ))}
        </div>

        {selectedTicket && (
          <div
            style={{
              marginTop: '30px',
              width: '80%',
              backgroundColor: '#ffffff',
              border: '1px solid #ccc',
              borderRadius: '8px',
              padding: '20px',
              boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)',
            }}
            ref={detailsRef}
          >
            <h2 style={{ color: '#333' }}>Detalhes do Ticket</h2>
            <p>
              <strong>Título:</strong> {selectedTicket.title}
            </p>
            <p>
              <strong>Descrição:</strong> {selectedTicket.description}
            </p>
            <p>
              <strong>Severidade:</strong>{' '}
              <span
                style={{ color: severityColors[selectedTicket.severity.level] }}
              >
                {selectedTicket.severity.description}
              </span>
            </p>
            <p>
              <strong>Status:</strong> {capitalizeWords(selectedTicket.status)}
            </p>
            {selectedTicket.comment && (
              <>
                <p>
                  <strong>Comentário:</strong> {selectedTicket.comment}
                </p>
                <p>
                  <strong>Usuário do Comentário:</strong>{' '}
                  {selectedTicket.comment_user}
                </p>
              </>
            )}
            <p>
              <strong>Criado em:</strong>{' '}
              {new Date(selectedTicket.created_at).toLocaleString()}
            </p>
            <p>
              <strong>Atualizado em:</strong>{' '}
              {new Date(selectedTicket.updated_at).toLocaleString()}
            </p>

            <h3 style={{ color: '#333' }}>Categorias e Subcategorias:</h3>
            {selectedTicket.categories.map((category) => (
              <div key={category.id}>
                <p>
                  <strong>Categoria:</strong> {category.name}
                </p>
                <ul>
                  {category.subcategories.map((subcategory) => (
                    <li key={subcategory.id}>{subcategory.name}</li>
                  ))}
                </ul>
              </div>
            ))}

            <div
              style={{
                display: 'flex',
                justifyContent: 'center',
                marginTop: '20px',
              }}
            >
              <button
                onClick={() => handleEdit(selectedTicket.id)}
                style={{
                  marginRight: '10px',
                  padding: '8px 16px',
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
                Editar
              </button>{' '}
              {userScopes.includes('admin') && (
                <>
                  <button
                    onClick={() => handleDelete(selectedTicket.id)}
                    style={{
                      marginRight: '10px',
                      padding: '8px 16px',
                      backgroundColor: '#f44336',
                      color: 'white',
                      border: 'none',
                      borderRadius: '5px',
                      cursor: 'pointer',
                      transition: 'background-color 0.3s ease',
                    }}
                    onMouseEnter={(e) =>
                      (e.currentTarget.style.backgroundColor = '#d32f2f')
                    }
                    onMouseLeave={(e) =>
                      (e.currentTarget.style.backgroundColor = '#f44336')
                    }
                  >
                    Deletar
                  </button>
                  <button
                    onClick={() => handleGenerateComment(selectedTicket.id)}
                    style={{
                      padding: '8px 16px',
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
                    Gerar Comentário
                  </button>
                </>
              )}
            </div>
          </div>
        )}

        {isCreateModalOpen && (
          <CreateTicketModal
            onClose={handleCloseCreateModal}
            onTicketCreated={handleTicketCreated}
          />
        )}

        {isEditModalOpen && selectedTicket && (
          <EditTicketModal
            ticket={selectedTicket}
            onClose={handleCloseEditModal}
            onTicketUpdated={handleTicketUpdated}
            modalRef={detailsRef}
          />
        )}
      </div>
    </div>
  );
};

export default Home;
