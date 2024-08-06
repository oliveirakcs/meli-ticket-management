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

api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (
      error.response &&
      error.response.status === 401
    ) {
      localStorage.removeItem('access_token');
      window.location.href = '/login';

      alert('Sessão expirou, faça novamente o login.');
    }

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

export const login = async (username: string, password: string) => {
  const loginData = new URLSearchParams();
  loginData.append('grant_type', 'password');
  loginData.append('username', username);
  loginData.append('password', password);
  loginData.append('scope', '');
  loginData.append('client_id', 'string');
  loginData.append('client_secret', 'string');

  try {
    const response = await api.post('/api/v1/login/', loginData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });

    return response.data;
  } catch (error) {
    handleApiError(error, 'Erro ao fazer login');
  }
};

// Users
export const fetchUsers = async () => {
  try {
    const response = await api.get('/api/v1/users');
    return response.data;
  } catch (error) {
    handleApiError(error, 'Erro ao buscar usuários');
  }
};

export const createUser = async (userData: any) => {
  try {
    const response = await api.post('/api/v1/users', userData);
    return response.data;
  } catch (error) {
    handleApiError(error, 'Erro ao criar usuário');
  }
};

export const updateUser = async (id: string, userData: any) => {
  try {
    const response = await api.patch(`/api/v1/users/${id}`, userData);
    return response.data;
  } catch (error) {
    handleApiError(error, 'Erro ao atualizar usuário');
  }
};

export const deleteUser = async (id: string) => {
  try {
    const response = await api.delete(`/api/v1/users/?user_id=${id}`);
    return response.data;
  } catch (error) {
    handleApiError(error, 'Erro ao deletar usuário');
  }
};

export const createRandomUser = async () => {
  try {
    const response = await api.post('/api/v1/users/create_random_user');
    return response.data;
  } catch (error) {
    handleApiError(error, 'Erro ao criar usuário aleatório');
  }
}

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

export const createCategory = async (categoryData: any) => {
  try {
    const response = await api.post('/api/v1/categories', categoryData);
    return response.data;
  } catch (error) {
    handleApiError(error, 'Erro ao criar categoria');
  }
};

export const updateCategory = async (id: string, categoryData: any) => {
  try {
    const response = await api.patch(`/api/v1/categories/${id}`, categoryData);
    return response.data;
  } catch (error) {
    handleApiError(error, 'Erro ao atualizar categoria');
  }
};

export const deleteCategory = async (id: string) => {
  try {
    const response = await api.delete(`/api/v1/categories/?category_id=${id}`);
    return response.data;
  } catch (error) {
    handleApiError(error, 'Erro ao deletar categoria');
  }
};

// Subcategories
export const fetchSubcategories = async () => {
  try {
    const response = await api.get('/api/v1/subcategories');
    return response.data;
  } catch (error) {
    handleApiError(error, 'Erro ao buscar subcategorias');
  }
};

// Subcategories
export const fetchSubcategoriesByCategory = async (categoryId: string) => {
  try {
    const response = await api.get(`/api/v1/subcategories/${categoryId}/show`);
    return response.data;
  } catch (error) {
    console.error('Erro ao buscar subcategorias:', error);
    throw new Error('Erro ao buscar subcategorias');
  }
};


export const createSubcategory = async (subcategoryData: any) => {
  try {
    const response = await api.post('/api/v1/subcategories', subcategoryData);
    return response.data;
  } catch (error) {
    handleApiError(error, 'Erro ao criar subcategoria');
  }
};

export const updateSubcategory = async (id: string, subcategoryData: any) => {
  try {
    const { name } = subcategoryData;

    const dataToUpdate = { name };
    const response = await api.patch(`/api/v1/subcategories/${id}`, dataToUpdate);
    
    return response.data;
  } catch (error) {
    handleApiError(error, 'Erro ao atualizar subcategoria');
  }
};

export const deleteSubcategory = async (id: string) => {
  try {
    const response = await api.delete(`/api/v1/subcategories/${id}`);
    return response.data;
  } catch (error) {
    handleApiError(error, 'Erro ao deletar subcategoria');
  }
};

// Severities
export const fetchSeverities = async () => {
  try {
    const response = await api.get('/api/v1/severities');
    return response.data;
  } catch (error) {
    handleApiError(error, 'Erro ao buscar Severities');
  }
};

export const createSeverity = async (severityData: any) => {
  try {
    const response = await api.post('/api/v1/severities', severityData);
    return response.data;
  } catch (error) {
    handleApiError(error, 'Erro ao criar severidade');
  }
};

export const updateSeverity = async (id: string, severityData: any) => {
  try {
    const response = await api.patch(`/api/v1/severities/${id}`, severityData);
    return response.data;
  } catch (error) {
    handleApiError(error, 'Erro ao atualizar severidade');
  }
};

export const deleteSeverity = async (id: string) => {
  try {
    const response = await api.delete(`/api/v1/severities/?severity_id=${id}`);
    return response.data;
  } catch (error) {
    handleApiError(error, 'Erro ao deletar severidade');
  }
};
