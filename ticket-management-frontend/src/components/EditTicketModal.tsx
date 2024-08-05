import React, { useState, useEffect } from 'react';
import { fetchSeverities, updateTicket } from '../services/api';
import { Ticket, Category, Subcategory, Severity } from '../types/ticketTypes';
import SelectCategoryModal from './SelectCategoryModal';

interface EditTicketModalProps {
  ticket: Ticket;
  onClose: () => void;
  onTicketUpdated: (updatedTicket: Ticket) => void;
  modalRef: React.RefObject<HTMLDivElement>;
}

const EditTicketModal: React.FC<EditTicketModalProps> = ({
  ticket,
  onClose,
  onTicketUpdated,
  modalRef,
}) => {
  const [title, setTitle] = useState(ticket.title);
  const [description, setDescription] = useState(ticket.description);
  const [
    selectedCategories,
    setSelectedCategories,
  ] = useState<{ category: Category; subcategories: Subcategory[] }[]>(
    ticket.categories.map((category) => ({
      category,
      subcategories: category.subcategories,
    }))
  );
  const [severities, setSeverities] = useState<Severity[]>([]);
  const [selectedSeverity, setSelectedSeverity] = useState(ticket.severity.id);
  const [selectedStatus, setSelectedStatus] = useState(ticket.status);
  const [isSelectCategoryModalOpen, setIsSelectCategoryModalOpen] = useState(false);
  const [hoveredCategoryId, setHoveredCategoryId] = useState<string | null>(null);

  useEffect(() => {
    const loadSeverities = async () => {
      try {
        const severityData = await fetchSeverities();
        setSeverities(severityData);
      } catch (error) {
        console.error('Erro ao buscar severidades:', error);
      }
    };

    loadSeverities();
  }, []);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (!title || !description || !selectedSeverity || selectedCategories.length === 0) {
      alert('Preencha todos os campos obrigatórios.');
      return;
    }

    const categoryIds = selectedCategories.map((cat) => cat.category.id);
    const subcategoryIds = selectedCategories.flatMap((cat) => cat.subcategories.map((sub) => sub.id));

    const updatedTicketData = {
      title,
      description,
      category_ids: categoryIds,
      subcategory_ids: subcategoryIds,
      severity_id: selectedSeverity,
      status: selectedStatus, // Include status in the update
    };

    try {
      const updatedTicket = await updateTicket(ticket.id, updatedTicketData);
      alert('Ticket atualizado com sucesso!');
      onTicketUpdated(updatedTicket);
      onClose(); // Close the modal after updating
    } catch (error: any) {
      console.error('Erro ao atualizar ticket:', error);
      alert('Erro ao atualizar ticket.');
    }
  };

  const handleAddCategory = (category: Category, subcategories: Subcategory[]) => {
    setSelectedCategories((prev) => [...prev, { category, subcategories }]);
  };

  return (
    <div className="modal-overlay" ref={modalRef}>
      <div className="modal-content create-ticket">
        <h2>Editar Ticket</h2>
        <form onSubmit={handleSubmit}>
          <div>
            <label>Título:</label>
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              required
            />
          </div>
          <div>
            <label>Descrição:</label>
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              required
            />
          </div>
          <div>
            <button type="button" onClick={() => setIsSelectCategoryModalOpen(true)}>
              Adicionar Categoria
            </button>
            {selectedCategories.length > 0 && (
              <div className="selected-categories">
                {selectedCategories.map(({ category, subcategories }) => (
                  <div
                    key={category.id}
                    className="selected-category"
                    onMouseEnter={() => setHoveredCategoryId(category.id)}
                    onMouseLeave={() => setHoveredCategoryId(null)}
                  >
                    <span>{category.name}</span>
                    <button type="button" onClick={() => setSelectedCategories((prev) => prev.filter(cat => cat.category.id !== category.id))}>
                      X
                    </button>
                    {hoveredCategoryId === category.id && (
                      <div className="subcategory-tooltip">
                        {subcategories.map((sub) => (
                          <div key={sub.id} className="subcategory-name">
                            {sub.name}
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
          <div>
            <label>Severidade:</label>
            <select
              value={selectedSeverity}
              onChange={(e) => setSelectedSeverity(e.target.value)}
              required
            >
              <option value="">Selecione a severidade</option>
              {severities.map((severity) => (
                <option key={severity.id} value={severity.id}>
                  {severity.description}
                </option>
              ))}
            </select>
          </div>
          
          <div>
            <label>Status:</label>
            <select
              value={selectedStatus}
              onChange={(e) => setSelectedStatus(e.target.value)}
              required
            >
              <option value="aberto">Aberto</option>
              <option value="em progresso">Em Progresso</option>
              <option value="resolvido">Resolvido</option>
            </select>
          </div>

          <div className="modal-actions">
            <button type="button" onClick={onClose}>
              Cancelar
            </button>
            <button type="submit">Atualizar Ticket</button>
          </div>
        </form>
      </div>
      {isSelectCategoryModalOpen && (
        <SelectCategoryModal
          onClose={() => setIsSelectCategoryModalOpen(false)}
          onAddCategory={handleAddCategory}
        />
      )}
    </div>
  );
};

export default EditTicketModal;
