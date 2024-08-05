import React from 'react';

interface TicketDetailsProps {
  ticket: {
    id: string;
    title: string;
    description: string;
    status: string;
    severity: {
      level: number;
      description: string;
    };
    created_at: string;
    updated_at: string | null;
    categories: { id: string; name: string }[];
    subcategories: { id: string; name: string }[];
  };
  onUpdateStatus: (status: string) => void;
  onDelete: () => void;
}

const TicketDetails: React.FC<TicketDetailsProps> = ({ ticket, onUpdateStatus, onDelete }) => {
  const { title, description, status, severity, created_at, updated_at, categories, subcategories } = ticket;

  const handleStatusChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    onUpdateStatus(e.target.value);
  };

  return (
    <div className="ticket-details">
      <h2>{title}</h2>
      <p><strong>Descrição:</strong> {description}</p>
      <p><strong>Status:</strong> {status}</p>
      <p><strong>Severidade:</strong> {severity.level} - {severity.description}</p>
      <p><strong>Criado em:</strong> {new Date(created_at).toLocaleString()}</p>
      <p><strong>Atualizado em:</strong> {updated_at ? new Date(updated_at).toLocaleString() : 'N/A'}</p>
      <p><strong>Categorias:</strong> {categories.map(cat => cat.name).join(', ')}</p>
      <p><strong>Subcategorias:</strong> {subcategories.map(sub => sub.name).join(', ')}</p>

      <div className="actions">
        <label>Atualizar Status:</label>
        <select value={status} onChange={handleStatusChange}>
          <option value="ABERTO">Aberto</option>
          <option value="EM_PROGRESSO">Em Progresso</option>
          <option value="RESOLVIDO">Resolvido</option>
        </select>

        <button onClick={onDelete} className="delete-button">
          Deletar Ticket
        </button>
      </div>
    </div>
  );
};

export default TicketDetails;
