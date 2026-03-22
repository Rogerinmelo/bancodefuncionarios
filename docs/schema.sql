-- Esquema inicial (MVP) para BNC de Funcionários

CREATE TABLE companies (
  id UUID PRIMARY KEY,
  name TEXT NOT NULL,
  cnpj VARCHAR(14),
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE users (
  id UUID PRIMARY KEY,
  company_id UUID NOT NULL REFERENCES companies(id),
  name TEXT NOT NULL,
  email TEXT NOT NULL,
  password_hash TEXT NOT NULL,
  role TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE employees (
  id UUID PRIMARY KEY,
  company_id UUID NOT NULL REFERENCES companies(id),
  full_name TEXT NOT NULL,
  cpf VARCHAR(11),
  phone TEXT,
  email TEXT,
  birth_date DATE,
  address TEXT,
  is_active BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE skills (
  id UUID PRIMARY KEY,
  company_id UUID NOT NULL REFERENCES companies(id),
  name TEXT NOT NULL,
  category TEXT,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE employee_skills (
  employee_id UUID NOT NULL REFERENCES employees(id),
  skill_id UUID NOT NULL REFERENCES skills(id),
  proficiency_level TEXT NOT NULL,
  years_experience NUMERIC(5,2),
  evidence_notes TEXT,
  PRIMARY KEY (employee_id, skill_id)
);

CREATE TABLE employee_education (
  id UUID PRIMARY KEY,
  employee_id UUID NOT NULL REFERENCES employees(id),
  type TEXT NOT NULL, -- curso, formacao, certificacao
  title TEXT NOT NULL,
  institution TEXT,
  start_date DATE,
  end_date DATE,
  certificate_expires_at DATE
);

CREATE TABLE services (
  id UUID PRIMARY KEY,
  company_id UUID NOT NULL REFERENCES companies(id),
  name TEXT NOT NULL,
  description TEXT
);

CREATE TABLE service_skill_requirements (
  service_id UUID NOT NULL REFERENCES services(id),
  skill_id UUID NOT NULL REFERENCES skills(id),
  priority TEXT NOT NULL, -- obrigatoria/desejavel
  PRIMARY KEY (service_id, skill_id)
);

CREATE TABLE demands (
  id UUID PRIMARY KEY,
  company_id UUID NOT NULL REFERENCES companies(id),
  service_id UUID REFERENCES services(id),
  title TEXT NOT NULL,
  description TEXT,
  type TEXT NOT NULL, -- demanda/licitação
  deadline DATE,
  location TEXT,
  budget NUMERIC(14,2),
  status TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE demand_skill_requirements (
  demand_id UUID NOT NULL REFERENCES demands(id),
  skill_id UUID NOT NULL REFERENCES skills(id),
  weight INTEGER NOT NULL DEFAULT 1,
  required BOOLEAN NOT NULL DEFAULT TRUE,
  PRIMARY KEY (demand_id, skill_id)
);

CREATE TABLE task_forces (
  id UUID PRIMARY KEY,
  demand_id UUID NOT NULL REFERENCES demands(id),
  name TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE task_force_members (
  task_force_id UUID NOT NULL REFERENCES task_forces(id),
  employee_id UUID NOT NULL REFERENCES employees(id),
  role_in_team TEXT,
  PRIMARY KEY (task_force_id, employee_id)
);

CREATE TABLE employee_service_history (
  id UUID PRIMARY KEY,
  employee_id UUID NOT NULL REFERENCES employees(id),
  service_id UUID REFERENCES services(id),
  demand_id UUID REFERENCES demands(id),
  comment TEXT,
  performed_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE employee_service_photos (
  id UUID PRIMARY KEY,
  history_id UUID NOT NULL REFERENCES employee_service_history(id),
  file_url TEXT NOT NULL,
  caption TEXT,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
