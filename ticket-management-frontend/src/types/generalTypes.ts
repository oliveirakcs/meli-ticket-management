
export interface Category {
  id: string;
  name: string;
  subcategories: Subcategory[];
}

export interface Subcategory {
  id: string;
  name: string;
  category_id: string;
}

export interface Severity {
  id: string;
  level: number;
  description: string;
}

export interface Ticket {
  id: string;
  title: string;
  description: string;
  categories: Category[];
  severity: Severity;
  status: string;
  comment: string;
  comment_user: string;
  created_at: string;
  updated_at: string;
}

// userTypes.ts

export interface User {
  id: string; // UUID is represented as a string
  name: string;
  username: string;
  email: string;
  password?: string; // Password is optional for update
  role: string;
}

// Omit 'id' and 'password' for user creation
export type UserCreation = Omit<User, 'id' | 'password'> & { password: string };

export interface Severity {
  id: string;
  level: number;
  description: string;
}

export interface SeverityCreation {
  level: number;
  description: string;
}

export interface Category {
  id: string;
  name: string;
  subcategories: Subcategory[];
}

export interface CategoryCreation {
  name: string;
}

export interface Subcategory {
  id: string;
  name: string;
  category_id: string;
}

export interface SubcategoryCreation {
  name: string;
  category_id: string;
}