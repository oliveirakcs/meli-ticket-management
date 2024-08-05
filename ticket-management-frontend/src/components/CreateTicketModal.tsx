import React, { useState } from 'react';
import { createTicket, fetchSeverities } from '../services/api';
import { Category, Subcategory, Severity } from '../types/ticketTypes';
import SelectCategoryModal from './SelectCategoryModal';

interface CreateTicketModalProps {
  onClose: () => void;
  onTicketCreated: () => void;
}

const CreateTicketModal: React.FC<CreateTicketModalProps> = ({ onClose, onTicketCreated }) => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [selectedCategories, setSelectedCategories] = useState<{ category: Category; subcategories: Subcategory[] }[]>([]);
  const [severities, setSeverities] = useState<Severity[]>([]);
  const [selectedSeverity, setSelectedSeverity] = useState<string>('');
  const [isSelectCategoryModalOpen, setIsSelectCategoryModalOpen] = useState(false);
  const [hoveredCategoryId, setHoveredCategoryId] = useState<string | null>(null);

  React.useEffect(() => {
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

    const newTicket = {
      title,
      description,
      category_ids: categoryIds,
      subcategory_ids: subcategoryIds,
      severity_id: selectedSeverity,
      status: 'aberto',
      comment: '',
      comment_user: ''
    };

    try {
      await createTicket(newTicket);
      alert('Ticket criado com sucesso!');
      onTicketCreated();
      onClose();
    } catch (error: any) {
      if (error.response && error.response.status === 400 && error.response.data.detail === 'Cannot create a ticket with severity level 1.') {
        alert('Nos casos que são muito urgentes, como severidade nível 1, entre em contato com a equipe de suporte de emergência.');
      } else {
        console.error('Erro ao criar ticket:', error);
        alert('Nos casos que são muito urgentes, como severidade nível 1, entre em contato com a equipe de suporte de emergência.');
      }
    }
  };

  const handleAddCategory = (category: Category, subcategories: Subcategory[]) => {
    setSelectedCategories((prev) => [...prev, { category, subcategories }]);
  };

  return (
    <div className="modal-overlay">
      <div className="modal-content create-ticket">
        <h2>Criar Novo Ticket</h2>
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
          <div className="modal-actions">
            <button type="button" onClick={onClose}>Cancelar</button>
            <button type="submit">Criar Ticket</button>
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

export default CreateTicketModal;
