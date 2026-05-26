## Getting Started

### Prerequisites
- Node.js 16+
- Python 3.9+
- PostgreSQL 12+
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/examace.git
cd examace
```

### 2. Backend Setup

#### Windows
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env
# Edit .env with your database credentials

# Run migrations
alembic upgrade head

# Start the server
uvicorn main:app --reload
```

#### Linux/Mac
```bash
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your database credentials

# Run migrations
alembic upgrade head

# Start the server
uvicorn main:app --reload
```

**Backend will run on**: http://localhost:8000

### 3. Database Setup

#### Windows
```bash
# Install PostgreSQL from https://www.postgresql.org/download/windows/
# Start PostgreSQL service

# Create database
psql -U postgres
CREATE DATABASE examace;
\q
```

#### Linux/Mac
```bash
# Install PostgreSQL
# macOS: brew install postgresql
# Ubuntu: sudo apt-get install postgresql

# Start PostgreSQL service
# macOS: brew services start postgresql
# Ubuntu: sudo service postgresql start

# Create database
createdb examace
```

### 4. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env file
copy .env.example .env

# Start development server
npm run dev
```

**Frontend will run on**: http://localhost:5173

### 5. Running with Docker (Optional)

```bash
cd docker
docker-compose up -d
```

This will start:
- Frontend on http://localhost
- Backend on http://localhost:8000
- PostgreSQL on localhost:5432
- Redis on localhost:6379

---

## Project Structure

```
examace/
├── frontend/              # React + Vite Frontend
│   ├── src/
│   │   ├── components/   # Reusable components
│   │   ├── pages/        # Page components
│   │   ├── services/     # API services
│   │   ├── hooks/        # Custom hooks
│   │   └── App.jsx
│   ├── package.json
│   └── vite.config.js
│
├── backend/              # FastAPI Backend
│   ├── app/
│   │   ├── auth/        # Authentication
│   │   ├── exams/       # Exam routes
│   │   ├── questions/   # Question routes
│   │   └── results/     # Result routes
│   ├── main.py
│   └── requirements.txt
│
├── database/            # Database schemas
│   └── schema.sql
│
└── docker/             # Docker configuration
    ├── docker-compose.yml
    └── Dockerfile.*
```

---

## Common Commands

### Backend
```bash
# Install new package
pip install package-name

# Add to requirements
pip freeze > requirements.txt

# Run tests
pytest

# Format code
black .

# Lint code
flake8 .
```

### Frontend
```bash
# Install new package
npm install package-name

# Run linter
npm run lint

# Format code
npm run format

# Build for production
npm run build

# Preview production build
npm run preview
```

---

## API Documentation

See [API.md](./docs/API.md) for complete API endpoints documentation.

---

## Architecture

See [ARCHITECTURE.md](./docs/ARCHITECTURE.md) for system architecture and design patterns.

---

## Database Schema

See [SCHEMA.md](./docs/SCHEMA.md) for database schema details.

---

## Contributing

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Commit changes: `git commit -m 'Add your feature'`
3. Push to branch: `git push origin feature/your-feature`
4. Open a Pull Request

---

## Troubleshooting

### Port Already in Use
- Frontend (5173): `npx kill-port 5173`
- Backend (8000): `npx kill-port 8000`

### Database Connection Error
- Check PostgreSQL is running
- Verify DATABASE_URL in .env
- Check database credentials

### Module Not Found
- Delete node_modules: `rm -rf node_modules`
- Reinstall: `npm install`

### Python Import Errors
- Ensure virtual environment is activated
- Reinstall requirements: `pip install -r requirements.txt`

---

## Deployment

### Frontend (Vercel)
```bash
npm run build
# Deploy dist/ folder to Vercel
```

### Backend (Railway)
- Push to GitHub
- Connect Railway to GitHub
- Deploy main branch

### Database (Supabase)
- Create Supabase project
- Import schema
- Update DATABASE_URL

---

## Resources

- [React Docs](https://react.dev)
- [FastAPI Docs](https://fastapi.tiangolo.com)
- [Tailwind CSS](https://tailwindcss.com)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)

---

## Support

For issues or questions:
1. Check existing GitHub issues
2. Create a new issue with details
3. Contact: your-email@example.com

---

**Happy Coding! 🚀**
