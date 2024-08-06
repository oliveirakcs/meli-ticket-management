import React, { useState, useEffect } from 'react';
import { fetchSeverities, updateTicket } from '../services/api';
import { Ticket, Category, Subcategory, Severity } from '../types/generalTypes';
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
  const [isSelectCategoryModalOpen, setIsSelectCategoryModalOpen] = useState(
    false
  );
  const [hoveredCategoryId, setHoveredCategoryId] = useState<string | null>(
    null
  );

  useEffect(() => {
    const loadSeverities = async () => {
      try {
        const severityData = await fetchSeverities();
        setSeverities(severityData);
      } catch (error) {
        console.error('Erro ao buscar Severities:', error);
      }
    };

    loadSeverities();
  }, []);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (
      !title ||
      !description ||
      !selectedSeverity ||
      selectedCategories.length === 0
    ) {
      alert('Preencha todos os campos obrigatórios.');
      return;
    }

    const categoryIds = selectedCategories.map((cat) => cat.category.id);
    const subcategoryIds = selectedCategories.flatMap((cat) =>
      cat.subcategories.map((sub) => sub.id)
    );

    const updatedTicketData = {
      title,
      description,
      category_ids: categoryIds,
      subcategory_ids: subcategoryIds,
      severity_id: selectedSeverity,
      status: selectedStatus,
    };

    try {
      const updatedTicket = await updateTicket(ticket.id, updatedTicketData);
      alert('Ticket atualizado com sucesso!');
      onTicketUpdated(updatedTicket);
      onClose();
    } catch (error: any) {
      console.error('Erro ao atualizar ticket:', error);
      alert('Erro ao atualizar ticket.');
    }
  };

  const handleAddCategory = (
    category: Category,
    subcategories: Subcategory[]
  ) => {
    setSelectedCategories((prev) => [...prev, { category, subcategories }]);
  };

  return (
    <div
      ref={modalRef}
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        backgroundColor: 'rgba(0, 0, 0, 0.5)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        zIndex: 1000,
      }}
    >
      <div
        style={{
          backgroundColor: '#fff',
          padding: '20px',
          borderRadius: '8px',
          boxShadow: '0 2px 10px rgba(0, 0, 0, 0.2)',
          maxWidth: '500px',
          width: '90%',
        }}
      >
        <h2 style={{ marginBottom: '20px' }}>Editar Ticket</h2>
        <form
          onSubmit={handleSubmit}
          style={{
            backgroundColor: '#fff',
            padding: '20px',
            borderRadius: '5px',
            boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)',
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
              Título:
            </label>
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
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
              Descrição:
            </label>
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              required
              style={{
                width: '100%',
                padding: '8px',
                borderRadius: '4px',
                border: '1px solid #ccc',
                boxSizing: 'border-box',
                resize: 'vertical',
              }}
            />
          </div>
          <div style={{ marginBottom: '20px' }}>
            <button
              type="button"
              onClick={() => setIsSelectCategoryModalOpen(true)}
              style={{
                backgroundColor: '#007bff',
                border: 'none',
                color: 'white',
                padding: '10px 20px',
                borderRadius: '5px',
                cursor: 'pointer',
                transition: 'background-color 0.3s ease',
                marginTop: '10px',
                textAlign: 'center',
                display: 'inline-block',
                fontSize: '16px',
                textDecoration: 'none',
              }}
              onMouseEnter={(e) =>
                (e.currentTarget.style.backgroundColor = '#0056b3')
              }
              onMouseLeave={(e) =>
                (e.currentTarget.style.backgroundColor = '#007bff')
              }
            >
              Adicionar Categoria
            </button>
            {selectedCategories.length > 0 && (
              <div
                style={{
                  display: 'flex',
                  flexWrap: 'wrap',
                  gap: '10px',
                  marginTop: '10px',
                }}
              >
                {selectedCategories.map(({ category, subcategories }) => (
                  <div
                    key={category.id}
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'space-between',
                      padding: '10px',
                      backgroundColor: '#e9ecef',
                      border: '1px solid #ccc',
                      borderRadius: '5px',
                      position: 'relative',
                      transition: 'box-shadow 0.3s ease',
                    }}
                    onMouseEnter={() => setHoveredCategoryId(category.id)}
                    onMouseLeave={() => setHoveredCategoryId(null)}
                  >
                    <span
                      style={{
                        flex: 1,
                        marginRight: '10px',
                        cursor: 'pointer',
                      }}
                    >
                      {category.name}
                    </span>
                    <button
                      type="button"
                      onClick={() =>
                        setSelectedCategories((prev) =>
                          prev.filter(
                            (cat) => cat.category.id !== category.id
                          )
                        )
                      }
                      style={{
                        backgroundColor: '#f44336',
                        color: 'white',
                        border: 'none',
                        padding: '5px 10px',
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
                      X
                    </button>
                    {hoveredCategoryId === category.id && (
                      <div
                        style={{
                          position: 'absolute',
                          backgroundColor: '#ffffff',
                          color: '#000000',
                          padding: '10px',
                          borderRadius: '5px',
                          border: '1px solid #ccc',
                          boxShadow: '0 2px 8px rgba(0, 0, 0, 0.2)',
                          zIndex: 100,
                          maxWidth: '90vw',
                          left: '50%',
                          transform: 'translateX(-50%)',
                          top: 'calc(100% + 5px)',
                          display: 'flex',
                          flexDirection: 'column',
                          gap: '1px',
                          whiteSpace: 'nowrap',
                          overflow: 'hidden',
                          textOverflow: 'ellipsis',
                        }}
                      >
                        {subcategories.map((sub) => (
                          <div
                            key={sub.id}
                            style={{
                              fontSize: '14px',
                              whiteSpace: 'nowrap',
                              overflow: 'hidden',
                              textOverflow: 'ellipsis',
                              display: 'block',
                              margin: '5px 0',
                              color: '#555',
                            }}
                          >
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
          <div style={{ marginBottom: '20px' }}>
            <label
              style={{
                display: 'block',
                fontWeight: 'bold',
                marginBottom: '8px',
                color: '#333',
              }}
            >
              Severidade:
            </label>
            <select
              value={selectedSeverity}
              onChange={(e) => setSelectedSeverity(e.target.value)}
              required
              style={{
                width: '100%',
                padding: '8px',
                borderRadius: '4px',
                border: '1px solid #ccc',
                boxSizing: 'border-box',
                marginBottom: '10px',
              }}
            >
              <option value="">Selecione a severidade</option>
              {severities.map((severity) => (
                <option key={severity.id} value={severity.id}>
                  {severity.description}
                </option>
              ))}
            </select>
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
              Status:
            </label>
            <select
              value={selectedStatus}
              onChange={(e) => setSelectedStatus(e.target.value)}
              required
              style={{
                width: '100%',
                padding: '8px',
                borderRadius: '4px',
                border: '1px solid #ccc',
                boxSizing: 'border-box',
                marginBottom: '10px',
              }}
            >
              <option value="aberto">Aberto</option>
              <option value="em progresso">Em Progresso</option>
              <option value="resolvido">Resolvido</option>
            </select>
          </div>

          <div
            style={{
              display: 'flex',
              justifyContent: 'flex-end',
              marginTop: '20px',
            }}
          >
            <button
              type="button"
              onClick={onClose}
              style={{
                backgroundColor: '#007bff',
                border: 'none',
                color: 'white',
                padding: '10px 20px',
                borderRadius: '5px',
                cursor: 'pointer',
                transition: 'background-color 0.3s ease',
                marginLeft: '10px',
              }}
              onMouseEnter={(e) =>
                (e.currentTarget.style.backgroundColor = '#0056b3')
              }
              onMouseLeave={(e) =>
                (e.currentTarget.style.backgroundColor = '#007bff')
              }
            >
              Cancelar
            </button>
            <button
              type="submit"
              style={{
                backgroundColor: '#007bff',
                color: 'white',
                padding: '10px 20px',
                border: 'none',
                borderRadius: '5px',
                cursor: 'pointer',
                transition: 'background-color 0.3s ease',
                marginLeft: '10px',
              }}
              onMouseEnter={(e) =>
                (e.currentTarget.style.backgroundColor = '#0056b3')
              }
              onMouseLeave={(e) =>
                (e.currentTarget.style.backgroundColor = '#007bff')
              }
            >
              Atualizar Ticket
            </button>
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
