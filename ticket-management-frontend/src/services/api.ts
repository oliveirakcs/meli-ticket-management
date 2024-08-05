import axios from 'axios';

const BASE_URL = 'http://localhost:1201';

const api = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers = config.headers || {};
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

const handleApiError = (error: any, message: string) => {
  if (axios.isAxiosError(error)) {
    console.error(`API Error: ${error.message}`);
  } else {
    console.error('An unexpected error occurred:', error);
  }
  throw new Error(message);
};

// Tickets
export const fetchTickets = async () => {
  try {
    const response = await api.get('/api/v1/tickets');
    return response.data;
  } catch (error) {
    handleApiError(error, 'Erro ao buscar tickets');
  }
};

export const fetchTicketById = async (id: string) => {
  try {
    const response = await api.get(`/api/v1/tickets/${id}`);
    return response.data;
  } catch (error) {
    handleApiError(error, 'Erro ao buscar ticket por ID');
  }
};

export const createTicket = async (ticketData: any) => {
  try {
    const response = await api.post('/api/v1/tickets', ticketData);
    return response.data;
  } catch (error) {
    handleApiError(error, 'Erro ao criar ticket');
  }
};

export const updateTicket = async (id: string, ticketData: any) => {
  try {
    const response = await api.patch(`/api/v1/tickets/${id}`, ticketData);
    return response.data;
  } catch (error) {
    handleApiError(error, 'Erro ao atualizar ticket');
  }
};

export const deleteTicket = async (id: string) => {
  try {
    const response = await api.delete(`/api/v1/tickets/?ticket_id=${id}`);
    return response.data;
  } catch (error) {
    handleApiError(error, 'Erro ao deletar ticket');
  }
};

export const generateComment = async (id: string) => {
  try {
    const response = await api.post(`/api/v1/tickets/add/${id}`);
    return response.data;
  } catch (error) {
    handleApiError(error, 'Erro ao gerar comentário');
  }
};

// Categories
export const fetchCategories = async () => {
  try {
    const response = await api.get('/api/v1/categories');
    return response.data;
  } catch (error) {
    handleApiError(error, 'Erro ao buscar categorias');
  }
};

// Subcategories
export const fetchSubcategories = async (categoryId: string) => {
  try {
    const response = await api.get(`/api/v1/subcategories/${categoryId}/show`);
    return response.data;
  } catch (error) {
    console.error('Erro ao buscar subcategorias:', error);
    throw new Error('Erro ao buscar subcategorias');
  }
};

// Severities
export const fetchSeverities = async () => {
  try {
    const response = await api.get('/api/v1/severities');
    return response.data;
  } catch (error) {
    handleApiError(error, 'Erro ao buscar severidades');
  }
};
