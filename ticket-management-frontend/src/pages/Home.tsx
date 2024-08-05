import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { fetchTickets, deleteTicket, generateComment } from '../services/api';
import TicketCard from '../components/TicketCard';
import CreateTicketModal from '../components/CreateTicketModal';
import EditTicketModal from '../components/EditTicketModal';
import { capitalizeWords } from '../utils/utils';

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
  const [isMenuOpen, setIsMenuOpen] = useState(false); // State for hamburger menu
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
      // Update the selected ticket with the new comment
      const updatedTicket = {
        ...selectedTicket!,
        comment,
        comment_user,
      };
      setSelectedTicket(updatedTicket);

      // Update the ticket list
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

  return (
    <div className="ticket-list">
      <div className="header">
        {userScopes.includes('admin') && (
          <div>
            <button
              className={`hamburger ${isMenuOpen ? 'open' : ''}`}
              onClick={() => setIsMenuOpen((prev) => !prev)}
            >
              &#9776;
            </button>
            {isMenuOpen && (
              <div className="menu">
                <ul>
                  <li onClick={() => handleNavigation('/severities')}>Severities</li>
                  <li onClick={() => handleNavigation('/users')}>Users</li>
                  <li onClick={() => handleNavigation('/categories')}>Categories</li>
                  <li onClick={() => handleNavigation('/subcategories')}>Subcategories</li>
                </ul>
              </div>
            )}
          </div>
        )}
        <button onClick={handleLogout} className="logout">
          Logout
        </button>
        <button onClick={handleCreateTicket} className="create-ticket">
          Criar Ticket
        </button>
      </div>
      <div className="card-container">
        {tickets.map((ticket) => (
          <TicketCard
            key={ticket.id}
            ticket={ticket}
            onClick={() => handleCardClick(ticket)}
            severityColor={severityColors[ticket.severity.level]}
          />
        ))}
      </div>

      {selectedTicket && (
        <div className="ticket-details" ref={detailsRef}>
          <h2>Detalhes do Ticket</h2>
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
                <strong>Usuário do Comentário:</strong> {selectedTicket.comment_user}
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

          <h3>Categorias e Subcategorias:</h3>
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

          <div className="button-container">
            <button onClick={() => handleEdit(selectedTicket.id)}>
              Editar
            </button>{' '}
            {userScopes.includes('admin') && (
              <>
                <button onClick={() => handleDelete(selectedTicket.id)}>
                  Deletar
                </button>
                <button onClick={() => handleGenerateComment(selectedTicket.id)}>
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
  );
};

export default Home;
