# Lesson Builder AI (Django)

Lesson Builder AI is a Django web application for generating, organizing, and reviewing lesson plans with AI assistance. It includes curriculum/resource management, calendar planning, and profile/authentication workflows.

## Current feature set

- User authentication (signup/login/password reset).
- Curriculum and resource management (PDF, DOCX, PPTX, TXT, CSV, JPG/JPEG/PNG with OCR).
- Lesson plan creation, edit, detail, and delete flows.
- Calendar-oriented lesson planning pages.
- AI-assisted chat/review workflow for lesson authoring.
- Material Kit-based UI with accessibility-focused overrides.

## Tech stack

- **Backend**: Django
- **Database**: SQLite (default), configurable for production
- **Frontend styling**: Material Kit CSS + Vite/PostCSS bundle for project overrides
- **Server**: Gunicorn + WhiteNoise-compatible static serving

## Local development setup

### 1) Clone and create environment

```bash
git clone <your-repo-url>
cd aisite
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\\Scripts\\activate
```

### 2) Install Python dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

> Note: dependency modernization targets are documented in `docs/DEPENDENCY_UPGRADE_PLAN.md`.

### 3) Configure environment

```bash
cp env.sample .env
```

Set required values in `.env` (e.g., `SECRET_KEY`, `DEBUG`, any AI provider keys).

### 4) Run migrations and start Django

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Visit: `http://127.0.0.1:8000/`

## Frontend build process (Vite + PostCSS)

A modern asset pipeline is provided for CSS/JS bundling and minification.

### Install and build

```bash
npm install
npm run build
```

Artifacts are emitted under `static/dist/`.

### Development mode

```bash
npm run dev
```

### What this build process provides

- CSS/JS bundling and minification.
- PostCSS with Autoprefixer for browser compatibility.
- Foundation for dead-code elimination/tree-shaking in JS bundles.
- Frontend test runner scaffold via Vitest (`npm test`).

## Deployment instructions

### Docker

```bash
docker compose up --build
```

### Render

- Use `render.yaml` for Blueprint deployment.
- Ensure environment variables are configured (`SECRET_KEY`, hosts, AI keys, etc.).
- Run migrations during release/start command.

### Production hardening checklist

- `DEBUG=False`
- Explicit `ALLOWED_HOSTS`
- Explicit `CSRF_TRUSTED_ORIGINS`
- Rotated `SECRET_KEY`
- HTTPS termination at proxy/load balancer

## API documentation

This project is primarily server-rendered. Existing AJAX endpoints are documented in:

- `docs/API.md`

## Testing and quality checks

```bash
python manage.py check
python manage.py test
npm test
```

Also see:

- `docs/CODE_REVIEW.md` for review findings and follow-up recommendations.
- `README_deploy.md` for additional deployment notes.
