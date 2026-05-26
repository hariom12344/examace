<!-- Use this file to provide workspace-specific custom instructions to Copilot. -->

# ExamAce Project Instructions

## Project Overview
ExamAce is an AI-powered competitive exam platform for IBPS, SBI, SSC, and other banking/government exams.

## Tech Stack
- **Frontend**: React + Vite + Tailwind CSS + Redux Toolkit
- **Backend**: FastAPI + SQLAlchemy + Pydantic
- **Database**: PostgreSQL
- **AI**: OpenAI API + LangChain
- **Deployment**: Docker, Vercel (frontend), Railway (backend), Supabase (database)

## Folder Structure
```
examace/
├── frontend/          # React SPA
├── backend/           # FastAPI API
├── database/          # SQL schemas
├── docker/            # Docker configs
├── docs/              # Documentation
└── .github/           # GitHub configs
```

## Development Guidelines

### Frontend Development
- Use functional components with React hooks
- Manage state with Redux Toolkit
- Style with Tailwind CSS classes
- Use React Query for data fetching
- Follow ESLint rules

### Backend Development
- Follow FastAPI best practices
- Use async/await for I/O operations
- Validate input with Pydantic models
- Use dependency injection for database sessions
- Document endpoints with docstrings

### Database
- Use PostgreSQL for all persistent data
- Create migrations with Alembic
- Index frequently queried columns
- Maintain referential integrity with foreign keys

## Current Phase
**Phase 1: Core Setup** - Authentication and database setup

## Next Steps
1. Initialize frontend: `npm install` in frontend folder
2. Initialize backend: `pip install -r requirements.txt` in backend folder
3. Setup PostgreSQL database
4. Run database migrations
5. Start development servers

## Important Files
- [README.md](./README.md) - Project overview
- [docs/SETUP.md](./docs/SETUP.md) - Setup instructions
- [docs/API.md](./docs/API.md) - API documentation
- [docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md) - System architecture
- [docs/ROADMAP.md](./docs/ROADMAP.md) - Development roadmap

## Useful Commands

### Frontend
```bash
cd frontend
npm install          # Install dependencies
npm run dev          # Start dev server
npm run build        # Build for production
npm run lint         # Run ESLint
npm run format       # Format with Prettier
```

### Backend
```bash
cd backend
pip install -r requirements.txt  # Install dependencies
uvicorn main:app --reload       # Start dev server
pytest                           # Run tests
black .                          # Format code
flake8 .                         # Run linter
```

### Database
```bash
# Run migrations
alembic upgrade head

# Create new migration
alembic revision --autogenerate -m "description"

# Create database
createdb examace

# Import schema
psql examace < database/schema.sql
```

## Code Style
- Python: Black formatter, 88 char line length
- JavaScript: Prettier formatter, 2 space indentation
- Commit messages: descriptive, present tense

## Testing
- Frontend: Vitest for unit tests
- Backend: Pytest for unit and integration tests
- Aim for >80% code coverage

## Deployment
- Frontend: Push to GitHub, auto-deploy to Vercel
- Backend: Push to GitHub, auto-deploy to Railway via webhook

## Resources
- [Copilot Help](https://github.com/features/copilot)
- [React Docs](https://react.dev)
- [FastAPI Docs](https://fastapi.tiangolo.com)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)
