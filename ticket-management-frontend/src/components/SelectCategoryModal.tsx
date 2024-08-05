import React, { useState, useEffect } from 'react';
import { fetchCategories, fetchSubcategories } from '../services/api';
import { Category, Subcategory } from '../types/ticketTypes';

interface SelectCategoryModalProps {
  onClose: () => void;
  onAddCategory: (category: Category, subcategories: Subcategory[]) => void;
}

const SelectCategoryModal: React.FC<SelectCategoryModalProps> = ({ onClose, onAddCategory }) => {
  const [categories, setCategories] = useState<Category[]>([]);
  const [subcategories, setSubcategories] = useState<Subcategory[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
  const [selectedSubcategories, setSelectedSubcategories] = useState<string[]>([]);

  useEffect(() => {
    const loadCategories = async () => {
      try {
        const categoryData = await fetchCategories();
        setCategories(categoryData);
      } catch (error) {
        console.error('Erro ao buscar categorias:', error);
      }
    };

    loadCategories();
  }, []);

  useEffect(() => {
    const loadSubcategories = async () => {
      if (selectedCategory) {
        try {
          const subcategoryData = await fetchSubcategories(selectedCategory);
          setSubcategories(subcategoryData);
        } catch (error) {
          console.error('Erro ao buscar subcategorias:', error);
        }
      }
    };

    loadSubcategories();
  }, [selectedCategory]);

  const handleAddCategory = () => {
    const category = categories.find((cat) => cat.id === selectedCategory);
    const subcats = subcategories.filter((sub) => selectedSubcategories.includes(sub.id));
    if (category && subcats.length > 0) {
      onAddCategory(category, subcats);
      onClose();
    }
  };

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <h2>Selecionar Categoria</h2>
        <div>
          <label>Categoria:</label>
          <select value={selectedCategory || ''} onChange={(e) => setSelectedCategory(e.target.value)}>
            <option value="" disabled>Selecione uma categoria</option>
            {categories.map((category) => (
              <option key={category.id} value={category.id}>{category.name}</option>
            ))}
          </select>
        </div>
        {selectedCategory && (
          <div>
            <label>Subcategorias:</label>
            <div className="subcategory-list">
              {subcategories.map((subcategory) => (
                <div key={subcategory.id} className="subcategory-item">
                  <input
                    type="checkbox"
                    id={`subcategory-${subcategory.id}`}
                    checked={selectedSubcategories.includes(subcategory.id)}
                    onChange={() => {
                      setSelectedSubcategories((prev) =>
                        prev.includes(subcategory.id)
                          ? prev.filter((id) => id !== subcategory.id)
                          : [...prev, subcategory.id]
                      );
                    }}
                  />
                  <label htmlFor={`subcategory-${subcategory.id}`}>{subcategory.name}</label>
                </div>
              ))}
            </div>
          </div>
        )}
        <div className="modal-actions">
          <button onClick={onClose}>Cancelar</button>
          <button onClick={handleAddCategory} disabled={!selectedCategory || selectedSubcategories.length === 0}>
            Adicionar Categoria
          </button>
        </div>
      </div>
    </div>
  );
};

export default SelectCategoryModal;
