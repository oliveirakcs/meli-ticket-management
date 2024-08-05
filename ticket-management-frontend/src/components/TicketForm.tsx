import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface Category {
  id: string;
  name: string;
}

interface Subcategory {
  id: string;
  name: string;
  category_id: string;
}

interface TicketFormProps {
  initialData?: {
    title: string;
    description: string;
    severity_id: string;
    category_ids: string[];
    subcategory_ids: string[];
  };
  onSubmit: (data: any) => void;
  buttonText: string;
}

const TicketForm: React.FC<TicketFormProps> = ({
  initialData = {
    title: '',
    description: '',
    severity_id: '',
    category_ids: [],
    subcategory_ids: [],
  },
  onSubmit,
  buttonText,
}) => {
  const [formData, setFormData] = useState(initialData);
  const [categories, setCategories] = useState<Category[]>([]);
  const [subcategories, setSubcategories] = useState<Subcategory[]>([]);

  useEffect(() => {
    fetchCategories();
  }, []);

  useEffect(() => {
    if (formData.category_ids.length > 0) {
      fetchSubcategories(formData.category_ids);
    } else {
      setSubcategories([]);
    }
  }, [formData.category_ids]);

  const fetchCategories = async () => {
    try {
      const response = await axios.get('http://localhost:1201/categories');
      setCategories(response.data);
    } catch (error) {
      console.error('Erro ao buscar categorias:', error);
    }
  };

  const fetchSubcategories = async (categoryIds: string[]) => {
    try {
      const promises = categoryIds.map((categoryId) =>
        axios.get(`http://localhost:1201/categories/${categoryId}/subcategories`)
      );
      const results = await Promise.all(promises);
      const subcategoriesData = results.flatMap(result => result.data);
      setSubcategories(subcategoriesData);
    } catch (error) {
      console.error('Erro ao buscar subcategorias:', error);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleMultiSelectChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const { options, name } = e.target;
    const selectedValues = Array.from(options)
      .filter(option => option.selected)
      .map(option => option.value);

    setFormData((prevData) => ({
      ...prevData,
      [name]: selectedValues,
    }));
  };

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label>Título:</label>
        <input
          type="text"
          name="title"
          value={formData.title}
          onChange={handleChange}
          required
        />
      </div>
      <div>
        <label>Descrição:</label>
        <textarea
          name="description"
          value={formData.description}
          onChange={handleChange}
          required
        />
      </div>
      <div>
        <label>Severidade:</label>
        <select
          name="severity_id"
          value={formData.severity_id}
          onChange={handleChange}
          required
        >
          <option value="">Selecione a Severidade</option>
          <option value="2">2 - High</option>
          <option value="3">3 - Medium</option>
          <option value="4">4 - Low</option>
        </select>
      </div>
      <div>
        <label>Categoria(s):</label>
        <select
          name="category_ids"
          multiple
          value={formData.category_ids}
          onChange={handleMultiSelectChange}
          required
        >
          {categories.map((category) => (
            <option key={category.id} value={category.id}>
              {category.name}
            </option>
          ))}
        </select>
      </div>
      <div>
        <label>Subcategoria(s):</label>
        <select
          name="subcategory_ids"
          multiple
          value={formData.subcategory_ids}
          onChange={handleMultiSelectChange}
        >
          {subcategories.map((subcategory) => (
            <option key={subcategory.id} value={subcategory.id}>
              {subcategory.name}
            </option>
          ))}
        </select>
      </div>
      <button type="submit">{buttonText}</button>
    </form>
  );
};

export default TicketForm;
