export type AuthTokens = {
  access_token: string;
  refresh_token: string;
  token_type: string;
};

export type Company = {
  id: string;
  name: string;
  cnpj?: string | null;
};

export type User = {
  id: string;
  company_id: string;
  name: string;
  email: string;
  role: string;
};

export type Employee = {
  id: string;
  full_name: string;
  cpf?: string | null;
  phone?: string | null;
  email?: string | null;
  is_active: boolean;
};

export type Skill = {
  id: string;
  name: string;
  category?: string | null;
};

export type Service = {
  id: string;
  name: string;
  description?: string | null;
};

export type Demand = {
  id: string;
  title: string;
  description?: string | null;
  status: string;
  type: string;
};

export type TeamSuggestionItem = {
  employee_id: string;
  employee_name: string;
  score: number;
  matched_required_skills: number;
  total_required_skills: number;
};

export type TeamSuggestionResponse = {
  demand_id: string;
  ranking: TeamSuggestionItem[];
};
