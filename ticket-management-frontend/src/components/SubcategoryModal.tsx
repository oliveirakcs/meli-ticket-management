import React, { useState } from 'react';
import { Subcategory, SubcategoryCreation } from '../types/generalTypes';

interface SubcategoryModalProps {
  subcategory: Subcategory | null;
  isEditMode: boolean;
  onClose: () => void;
  onSubmit: (subcategory: Subcategory | SubcategoryCreation) => void;
  category_id: string;
}

const SubcategoryModal: React.FC<SubcategoryModalProps> = ({
  subcategory,
  isEditMode,
  onClose,
  onSubmit,
  category_id,
}) => {
  const [name, setName] = useState(subcategory?.name || '');

  const handleSubmit = () => {
    if (name.trim() === '') {
      alert('O nome da subcategoria é obrigatório.');
      return;
    }

    const newSubcategory = {
      ...(isEditMode ? { id: subcategory?.id } : {}),
      name,
      category_id,
    };

    onSubmit(newSubcategory as Subcategory | SubcategoryCreation);
    onClose();
  };

  return (
    <div
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: 'rgba(0, 0, 0, 0.5)',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        zIndex: 1000,
      }}
    >
      <div
        style={{
          backgroundColor: 'white',
          padding: '20px',
          borderRadius: '8px',
          width: '400px',
          maxWidth: 'calc(100% - 40px)', // Ajuste para evitar estouro em telas menores
          boxShadow: '0 4px 8px rgba(0, 0, 0, 0.2)',
          textAlign: 'center',
          boxSizing: 'border-box', // Certifique-se de que o padding está incluído na largura total
        }}
      >
        <h2>{isEditMode ? 'Editar Subcategoria' : 'Criar Subcategoria'}</h2>
        <input
          type="text"
          placeholder="Nome da Subcategoria"
          value={name}
          onChange={(e) => setName(e.target.value)}
          style={{
            width: '100%', // Ajuste para garantir que o input ocupe 100% da largura do modal
            padding: '10px',
            marginBottom: '20px',
            borderRadius: '4px',
            border: '1px solid #ccc',
            outline: 'none',
            fontSize: '16px',
            boxSizing: 'border-box', // Inclui o padding na largura total do input
          }}
        />
        <button
          onClick={handleSubmit}
          style={{
            backgroundColor: '#007bff',
            border: 'none',
            padding: '10px 20px',
            borderRadius: '5px',
            color: 'white',
            cursor: 'pointer',
            transition: 'background-color 0.3s ease',
            fontSize: '16px',
            boxShadow: '0 2px 4px rgba(0, 0, 0, 0.2)',
            outline: 'none',
            marginRight: '10px',
          }}
          onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = '#0056b3')}
          onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = '#007bff')}
        >
          {isEditMode ? 'Atualizar' : 'Criar'}
        </button>
        <button
          onClick={onClose}
          style={{
            backgroundColor: '#f44336',
            border: 'none',
            padding: '10px 20px',
            borderRadius: '5px',
            color: 'white',
            cursor: 'pointer',
            transition: 'background-color 0.3s ease',
            fontSize: '16px',
            boxShadow: '0 2px 4px rgba(0, 0, 0, 0.2)',
            outline: 'none',
          }}
          onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = '#d32f2f')}
          onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = '#f44336')}
        >
          Cancelar
        </button>
      </div>
    </div>
  );
};

export default SubcategoryModal;
