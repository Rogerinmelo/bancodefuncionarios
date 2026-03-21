import type {
  AuthTokens,
  Company,
  Demand,
  Employee,
  Service,
  Skill,
  TeamSuggestionResponse,
  User,
} from "./types";

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000/api/v1";

async function parseResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const payload = await response.json().catch(() => ({ detail: "Erro inesperado" }));
    throw new Error(payload.detail ?? "Erro inesperado");
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return (await response.json()) as T;
}

function authHeaders(token: string): HeadersInit {
  return {
    Authorization: `Bearer ${token}`,
  };
}

export const api = {
  registerCompany: async (name: string, cnpj: string): Promise<Company> => {
    const response = await fetch(`${API_BASE}/auth/register-company`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, cnpj: cnpj || null }),
    });
    return parseResponse<Company>(response);
  },

  registerUser: async (params: {
    companyId: string;
    name: string;
    email: string;
    password: string;
    role: "admin" | "gestor" | "viewer";
  }): Promise<User> => {
    const response = await fetch(`${API_BASE}/auth/register-user`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        company_id: params.companyId,
        name: params.name,
        email: params.email,
        password: params.password,
        role: params.role,
      }),
    });
    return parseResponse<User>(response);
  },

  login: async (companyId: string, email: string, password: string): Promise<AuthTokens> => {
    const response = await fetch(`${API_BASE}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ company_id: companyId, email, password }),
    });
    return parseResponse<AuthTokens>(response);
  },

  me: async (token: string): Promise<User> => {
    const response = await fetch(`${API_BASE}/auth/me`, {
      headers: authHeaders(token),
    });
    return parseResponse<User>(response);
  },

  listEmployees: async (token: string): Promise<Employee[]> => {
    const response = await fetch(`${API_BASE}/employees`, { headers: authHeaders(token) });
    return parseResponse<Employee[]>(response);
  },

  createEmployee: async (
    token: string,
    payload: { full_name: string; cpf?: string; phone?: string; email?: string },
  ): Promise<Employee> => {
    const response = await fetch(`${API_BASE}/employees`, {
      method: "POST",
      headers: { ...authHeaders(token), "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    return parseResponse<Employee>(response);
  },

  listSkills: async (token: string): Promise<Skill[]> => {
    const response = await fetch(`${API_BASE}/skills`, { headers: authHeaders(token) });
    return parseResponse<Skill[]>(response);
  },

  createSkill: async (token: string, payload: { name: string; category?: string }): Promise<Skill> => {
    const response = await fetch(`${API_BASE}/skills`, {
      method: "POST",
      headers: { ...authHeaders(token), "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    return parseResponse<Skill>(response);
  },

  listServices: async (token: string): Promise<Service[]> => {
    const response = await fetch(`${API_BASE}/services`, { headers: authHeaders(token) });
    return parseResponse<Service[]>(response);
  },

  createService: async (token: string, payload: { name: string; description?: string }): Promise<Service> => {
    const response = await fetch(`${API_BASE}/services`, {
      method: "POST",
      headers: { ...authHeaders(token), "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    return parseResponse<Service>(response);
  },

  listDemands: async (token: string): Promise<Demand[]> => {
    const response = await fetch(`${API_BASE}/demands`, { headers: authHeaders(token) });
    return parseResponse<Demand[]>(response);
  },

  createDemand: async (
    token: string,
    payload: { title: string; description?: string; type?: string; status?: string },
  ): Promise<Demand> => {
    const response = await fetch(`${API_BASE}/demands`, {
      method: "POST",
      headers: { ...authHeaders(token), "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    return parseResponse<Demand>(response);
  },

  suggestTeam: async (token: string, demandId: string): Promise<TeamSuggestionResponse> => {
    const response = await fetch(`${API_BASE}/demands/${demandId}/suggest-team`, {
      method: "POST",
      headers: authHeaders(token),
    });
    return parseResponse<TeamSuggestionResponse>(response);
  },
};
