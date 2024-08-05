import React from 'react';
import { Ticket } from '../pages/Home';
import { capitalizeWords } from '../utils/utils';

interface TicketCardProps {
  ticket: Ticket;
  onClick: () => void;
  severityColor: string;
}

const TicketCard: React.FC<TicketCardProps> = ({ ticket, onClick, severityColor }) => {

  return (
    <div className="ticket-card" onClick={onClick} style={{ borderColor: severityColor }}>
      <h2>{ticket.title}</h2>
      <p>
        <strong>Severidade:</strong>{' '}
        <span style={{ color: severityColor }}>{ticket.severity.description}</span>
      </p>
      <p>
        <strong>Criado em:</strong>{' '}
        <span>{new Date(ticket.created_at).toLocaleString()}</span>
      </p>
      <p>
      <strong>Status:</strong> {capitalizeWords(ticket.status)}
        </p>
    </div>
  );
};

export default TicketCard;
