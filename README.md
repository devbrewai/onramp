# Onramp

AI-powered KYC document intake for fintech onboarding. Upload an identity, address, or income document and get back classified, extracted, and validated structured data with per-field confidence scores and an overall risk score.

Built by [Devbrew](https://devbrew.ai).

## Tech Stack

- **Frontend:** React 19, TypeScript, Vite, Tailwind CSS, shadcn/ui
- **Backend:** Python 3.11, FastAPI, Pydantic AI
- **LLM:** Claude Sonnet 4.6 (vision) — single call handles classification + extraction
- **PDF Rendering:** PyMuPDF

## Quick Start

### Backend

```bash
cd backend
cp .env.example .env          # Add your ANTHROPIC_API_KEY
uv sync                       # Install dependencies
uv run uvicorn app.main:app --reload --port 8001
```

### Frontend

```bash
cd frontend
bun install                   # Install dependencies
bun dev                       # Starts on http://localhost:5173
```

The Vite dev server proxies `/api` requests to `localhost:8001`.

## Environment Variables

### Backend (`backend/.env`)

| Variable            | Required | Default                 | Description                     |
| ------------------- | -------- | ----------------------- | ------------------------------- |
| `ANTHROPIC_API_KEY` | Yes      | —                       | Claude API key                  |
| `CORS_ORIGINS`      | No       | `http://localhost:5173` | Comma-separated allowed origins |
| `LOG_LEVEL`         | No       | `info`                  | Logging level                   |
| `MAX_FILE_SIZE_MB`  | No       | `10`                    | Upload size cap                 |

### Frontend (`frontend/.env`)

| Variable       | Required | Default | Description                             |
| -------------- | -------- | ------- | --------------------------------------- |
| `VITE_API_URL` | No       | —       | Backend URL (leave empty for dev proxy) |

## Deployment

### Backend → Render

The repo includes a `render.yaml` Blueprint for one-click deployment:

1. Connect the repo on [Render](https://render.com)
2. Set environment variables: `ANTHROPIC_API_KEY`, `CORS_ORIGINS`
3. Render auto-detects `render.yaml` and configures the service

### Frontend → Vercel

1. Connect the repo on [Vercel](https://vercel.com)
2. Set root directory to `frontend/`
3. Set environment variable: `VITE_API_URL` (Render backend URL)
4. Vercel auto-detects Vite and builds

## Architecture

See [Architecture Decision Records](docs/adr/README.md) for detailed design rationale.

```
POST /api/process → Ingest → PDF→Image → LLM Vision Extract → Validate → Risk Score → Response
GET  /api/samples → List pre-loaded sample documents
GET  /api/health  → Status check
```

## License

MIT
