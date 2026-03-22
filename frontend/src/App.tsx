import { FormEvent, useEffect, useMemo, useState } from "react";

import { Card } from "./components/Card";
import { api } from "./lib/api";
import type { Demand, Employee, Service, Skill, TeamSuggestionResponse, User } from "./lib/types";

type Session = {
  accessToken: string;
  refreshToken: string;
  user: User;
};

const STORAGE_KEY = "bnc_front_session";

function App() {
  const [session, setSession] = useState<Session | null>(null);
  const [statusMessage, setStatusMessage] = useState<string>("Conecte sua conta para começar.");
  const [isLoading, setIsLoading] = useState(false);

  const [employees, setEmployees] = useState<Employee[]>([]);
  const [skills, setSkills] = useState<Skill[]>([]);
  const [services, setServices] = useState<Service[]>([]);
  const [demands, setDemands] = useState<Demand[]>([]);
  const [suggestion, setSuggestion] = useState<TeamSuggestionResponse | null>(null);

  useEffect(() => {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return;

    try {
      setSession(JSON.parse(raw) as Session);
    } catch {
      localStorage.removeItem(STORAGE_KEY);
    }
  }, []);

  useEffect(() => {
    if (!session) return;
    localStorage.setItem(STORAGE_KEY, JSON.stringify(session));
  }, [session]);

  const sortedDemands = useMemo(() => [...demands].sort((a, b) => a.title.localeCompare(b.title)), [demands]);

  const loadData = async (token: string) => {
    const [emp, skl, srv, dmd] = await Promise.all([
      api.listEmployees(token),
      api.listSkills(token),
      api.listServices(token),
      api.listDemands(token),
    ]);
    setEmployees(emp);
    setSkills(skl);
    setServices(srv);
    setDemands(dmd);
  };

  const handleBootstrap = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setIsLoading(true);
    setStatusMessage("Criando empresa e usuário admin...");

    const form = new FormData(event.currentTarget);
    const companyName = String(form.get("companyName") ?? "").trim();
    const companyCnpj = String(form.get("companyCnpj") ?? "").trim();
    const userName = String(form.get("userName") ?? "").trim();
    const userEmail = String(form.get("userEmail") ?? "").trim();
    const password = String(form.get("password") ?? "");

    try {
      const company = await api.registerCompany(companyName, companyCnpj);
      await api.registerUser({
        companyId: company.id,
        name: userName,
        email: userEmail,
        password,
        role: "admin",
      });
      setStatusMessage(`Empresa criada com sucesso. ID: ${company.id}`);
    } catch (error) {
      setStatusMessage((error as Error).message);
    } finally {
      setIsLoading(false);
    }
  };

  const handleLogin = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setIsLoading(true);

    const form = new FormData(event.currentTarget);
    const companyId = String(form.get("companyId") ?? "").trim();
    const email = String(form.get("email") ?? "").trim();
    const password = String(form.get("password") ?? "");

    try {
      const tokens = await api.login(companyId, email, password);
      const me = await api.me(tokens.access_token);
      const nextSession: Session = {
        accessToken: tokens.access_token,
        refreshToken: tokens.refresh_token,
        user: me,
      };
      setSession(nextSession);
      await loadData(tokens.access_token);
      setStatusMessage(`Sessão iniciada para ${me.name} (${me.role}).`);
    } catch (error) {
      setStatusMessage((error as Error).message);
    } finally {
      setIsLoading(false);
    }
  };

  const handleLogout = () => {
    setSession(null);
    setEmployees([]);
    setSkills([]);
    setServices([]);
    setDemands([]);
    setSuggestion(null);
    localStorage.removeItem(STORAGE_KEY);
    setStatusMessage("Sessão finalizada.");
  };

  const handleQuickCreate = async (
    event: FormEvent<HTMLFormElement>,
    entity: "employee" | "skill" | "service" | "demand",
  ) => {
    event.preventDefault();
    if (!session) return;

    setIsLoading(true);
    const form = new FormData(event.currentTarget);

    try {
      if (entity === "employee") {
        await api.createEmployee(session.accessToken, {
          full_name: String(form.get("full_name") ?? ""),
          cpf: String(form.get("cpf") ?? "") || undefined,
          phone: String(form.get("phone") ?? "") || undefined,
          email: String(form.get("email") ?? "") || undefined,
        });
      }

      if (entity === "skill") {
        await api.createSkill(session.accessToken, {
          name: String(form.get("name") ?? ""),
          category: String(form.get("category") ?? "") || undefined,
        });
      }

      if (entity === "service") {
        await api.createService(session.accessToken, {
          name: String(form.get("name") ?? ""),
          description: String(form.get("description") ?? "") || undefined,
        });
      }

      if (entity === "demand") {
        await api.createDemand(session.accessToken, {
          title: String(form.get("title") ?? ""),
          description: String(form.get("description") ?? "") || undefined,
          type: String(form.get("type") ?? "demanda"),
          status: String(form.get("status") ?? "aberta"),
        });
      }

      await loadData(session.accessToken);
      event.currentTarget.reset();
      setStatusMessage("Registro criado com sucesso.");
    } catch (error) {
      setStatusMessage((error as Error).message);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSuggestTeam = async (demandId: string) => {
    if (!session) return;
    setIsLoading(true);
    try {
      const result = await api.suggestTeam(session.accessToken, demandId);
      setSuggestion(result);
      setStatusMessage("Sugestão de equipe gerada com sucesso.");
    } catch (error) {
      setStatusMessage((error as Error).message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="container">
      <header className="hero">
        <div>
          <h1>BNC Funcionários</h1>
          <p>Painel inicial para gestão de equipe multiempresa.</p>
        </div>
        {session && (
          <button className="button secondary" onClick={handleLogout} type="button">
            Sair
          </button>
        )}
      </header>

      <p className="status">{statusMessage}</p>

      {!session ? (
        <div className="grid two-columns">
          <Card title="1) Criar empresa + usuário admin">
            <form className="form" onSubmit={handleBootstrap}>
              <input name="companyName" placeholder="Nome da empresa" required />
              <input name="companyCnpj" placeholder="CNPJ (opcional)" />
              <input name="userName" placeholder="Nome do administrador" required />
              <input name="userEmail" type="email" placeholder="Email" required />
              <input name="password" type="password" placeholder="Senha" minLength={6} required />
              <button className="button" disabled={isLoading} type="submit">
                Criar cadastro inicial
              </button>
            </form>
          </Card>

          <Card title="2) Entrar no sistema">
            <form className="form" onSubmit={handleLogin}>
              <input name="companyId" placeholder="Company ID" required />
              <input name="email" type="email" placeholder="Email" required />
              <input name="password" type="password" placeholder="Senha" required />
              <button className="button" disabled={isLoading} type="submit">
                Entrar
              </button>
            </form>
          </Card>
        </div>
      ) : (
        <>
          <section className="session-summary">
            <strong>{session.user.name}</strong> · {session.user.email} · perfil <strong>{session.user.role}</strong>
          </section>

          <div className="grid two-columns">
            <Card title={`Funcionários (${employees.length})`}>
              <form className="form compact" onSubmit={(event) => handleQuickCreate(event, "employee")}>
                <input name="full_name" placeholder="Nome completo" required />
                <input name="cpf" placeholder="CPF" />
                <input name="phone" placeholder="Telefone" />
                <input name="email" placeholder="Email" type="email" />
                <button className="button" disabled={isLoading} type="submit">
                  Adicionar funcionário
                </button>
              </form>
              <ul>
                {employees.map((employee) => (
                  <li key={employee.id}>{employee.full_name}</li>
                ))}
              </ul>
            </Card>

            <Card title={`Habilidades (${skills.length})`}>
              <form className="form compact" onSubmit={(event) => handleQuickCreate(event, "skill")}>
                <input name="name" placeholder="Nome da habilidade" required />
                <input name="category" placeholder="Categoria" />
                <button className="button" disabled={isLoading} type="submit">
                  Adicionar habilidade
                </button>
              </form>
              <ul>
                {skills.map((skill) => (
                  <li key={skill.id}>{skill.name}</li>
                ))}
              </ul>
            </Card>

            <Card title={`Serviços (${services.length})`}>
              <form className="form compact" onSubmit={(event) => handleQuickCreate(event, "service")}>
                <input name="name" placeholder="Nome do serviço" required />
                <input name="description" placeholder="Descrição" />
                <button className="button" disabled={isLoading} type="submit">
                  Adicionar serviço
                </button>
              </form>
              <ul>
                {services.map((service) => (
                  <li key={service.id}>{service.name}</li>
                ))}
              </ul>
            </Card>

            <Card title={`Demandas (${demands.length})`}>
              <form className="form compact" onSubmit={(event) => handleQuickCreate(event, "demand")}>
                <input name="title" placeholder="Título da demanda" required />
                <input name="description" placeholder="Descrição" />
                <input name="type" defaultValue="demanda" placeholder="Tipo" />
                <input name="status" defaultValue="aberta" placeholder="Status" />
                <button className="button" disabled={isLoading} type="submit">
                  Adicionar demanda
                </button>
              </form>
              <ul>
                {sortedDemands.map((demand) => (
                  <li key={demand.id}>
                    <div className="inline-between">
                      <span>{demand.title}</span>
                      <button
                        className="link-button"
                        disabled={isLoading}
                        onClick={() => handleSuggestTeam(demand.id)}
                        type="button"
                      >
                        Sugerir equipe
                      </button>
                    </div>
                  </li>
                ))}
              </ul>
            </Card>
          </div>

          <Card title="Sugestão de equipe (última execução)">
            {!suggestion ? (
              <p>Selecione “Sugerir equipe” em uma demanda para ver o ranking.</p>
            ) : (
              <ol>
                {suggestion.ranking.map((item) => (
                  <li key={item.employee_id}>
                    {item.employee_name} — score {item.score.toFixed(2)} ({item.matched_required_skills}/
                    {item.total_required_skills} skills obrigatórias)
                  </li>
                ))}
              </ol>
            )}
          </Card>
        </>
      )}
    </main>
  );
}

export default App;
