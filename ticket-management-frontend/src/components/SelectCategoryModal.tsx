import React, { useState, useEffect } from 'react';
import { fetchCategories, fetchSubcategoriesByCategory } from '../services/api';
import { Category, Subcategory } from '../types/generalTypes';

interface SelectCategoryModalProps {
  onClose: () => void;
  onAddCategory: (category: Category, subcategories: Subcategory[]) => void;
}

const SelectCategoryModal: React.FC<SelectCategoryModalProps> = ({
  onClose,
  onAddCategory,
}) => {
  const [categories, setCategories] = useState<Category[]>([]);
  const [subcategories, setSubcategories] = useState<Subcategory[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
  const [selectedSubcategories, setSelectedSubcategories] = useState<string[]>(
    []
  );

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
          const subcategoryData = await fetchSubcategoriesByCategory(selectedCategory);
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
    const subcats = subcategories.filter((sub) =>
      selectedSubcategories.includes(sub.id)
    );
    if (category && subcats.length > 0) {
      onAddCategory(category, subcats);
      onClose();
    }
  };

  return (
    <div
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
        <h2 style={{ marginBottom: '20px' }}>Selecionar Categoria</h2>
        <div style={{ marginBottom: '20px' }}>
          <label
            style={{
              display: 'block',
              fontWeight: 'bold',
              marginBottom: '8px',
              color: '#333',
            }}
          >
            Categoria:
          </label>
          <select
            value={selectedCategory || ''}
            onChange={(e) => setSelectedCategory(e.target.value)}
            style={{
              width: '100%',
              padding: '8px',
              borderRadius: '4px',
              border: '1px solid #ccc',
              boxSizing: 'border-box',
            }}
          >
            <option value="" disabled>
              Selecione uma categoria
            </option>
            {categories.map((category) => (
              <option key={category.id} value={category.id}>
                {category.name}
              </option>
            ))}
          </select>
        </div>
        {selectedCategory && (
          <div style={{ marginBottom: '20px' }}>
            <label
              style={{
                display: 'block',
                fontWeight: 'bold',
                marginBottom: '8px',
                color: '#333',
              }}
            >
              Subcategorias:
            </label>
            <div
              style={{
                display: 'flex',
                flexWrap: 'wrap',
                gap: '2px',
                marginTop: '10px',
                marginBottom: '20px',
              }}
            >
              {subcategories.map((subcategory) => (
                <div
                  key={subcategory.id}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    width: 'calc(50% - 15px)',
                    boxSizing: 'border-box',
                    marginBottom: '10px',
                    position: 'relative',
                    cursor: 'pointer',
                  }}
                >
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
                    style={{
                      marginRight: '10px',
                    }}
                  />
                  <label
                    htmlFor={`subcategory-${subcategory.id}`}
                    style={{
                      color: '#555',
                      display: 'block',
                      margin: '5px 0',
                    }}
                  >
                    {subcategory.name}
                  </label>
                </div>
              ))}
            </div>
          </div>
        )}
        <div
          style={{
            display: 'flex',
            justifyContent: 'flex-end',
            marginTop: '20px',
          }}
        >
          <button
            onClick={onClose}
            style={{
              backgroundColor: '#007bff',
              border: 'none',
              color: 'white',
              padding: '10px 20px',
              borderRadius: '5px',
              cursor: 'pointer',
              transition: 'background-color 0.3s ease',
              marginRight: '10px',
              marginBottom: '20px',

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
            onClick={handleAddCategory}
            disabled={!selectedCategory || selectedSubcategories.length === 0}
            style={{
              backgroundColor: '#007bff',
              color: 'white',
              padding: '10px 20px',
              borderRadius: '5px',
              border: 'none',
              cursor: 'pointer',
              marginBottom: '20px',
              display: 'block',
              marginLeft: '10px',
              transition: 'background-color 0.3s ease',
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
        </div>
      </div>
    </div>
  );
};

export default SelectCategoryModal;
