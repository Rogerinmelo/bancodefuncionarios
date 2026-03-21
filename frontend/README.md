# Frontend (React + Vite + TypeScript)

Interface web inicial para operar os módulos já existentes no backend:

- Bootstrap de tenant (criar empresa + usuário admin)
- Login JWT
- Listagem e cadastro rápido de funcionários, habilidades, serviços e demandas
- Acionamento da sugestão de equipe por demanda

## Rodando localmente

```bash
cd frontend
cp .env.example .env
npm install
npm run dev
```

A aplicação sobe em `http://127.0.0.1:5173`.

## Build de produção

```bash
npm run build
npm run preview
```

## Variáveis

- `VITE_API_BASE_URL`: URL base da API (default `http://127.0.0.1:8000/api/v1`).
