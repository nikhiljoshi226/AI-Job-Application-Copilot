# AI Job Application Copilot

An AI-powered job application copilot that helps users optimize their job search through intelligent resume analysis, job description parsing, personalized content generation, and interview preparation.

## Features

- **Resume Analysis**: Parse and analyze resumes to extract skills, experience, and achievements
- **Job Description Analysis**: Extract requirements, skills, and company insights from job descriptions
- **Resume Tailoring**: Generate personalized resume improvements based on job requirements
- **Cover Letter Generation**: Create tailored cover letters and outreach content
- **Interview Preparation**: Generate likely questions and STAR-format stories based on user experience
- **Application Tracking**: Track applications throughout the entire hiring process

## Architecture

- **Frontend**: Next.js 14 with TypeScript, Tailwind CSS, and shadcn/ui
- **Backend**: FastAPI with Python, PostgreSQL database, and async processing
- **AI Integration**: OpenAI/Anthropic APIs for content generation
- **Database**: PostgreSQL with Prisma ORM

## Quick Start

### Prerequisites

- Node.js 18+ and npm
- Python 3.11+ and pip
- PostgreSQL (or use Docker)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ai-job-application-copilot
```

2. Install all dependencies:
```bash
npm run setup
```

3. Set up environment variables:
```bash
# Frontend
cp frontend/.env.example frontend/.env.local

# Backend
cp backend/.env.example backend/.env
```

4. Start the development servers:
```bash
npm run dev
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Development Scripts

- `npm run dev` - Start both frontend and backend in development mode
- `npm run dev:frontend` - Start only frontend development server
- `npm run dev:backend` - Start only backend development server
- `npm run build` - Build both frontend and backend for production
- `npm run test` - Run all tests
- `npm run lint` - Run linting for both frontend and backend
- `npm run format` - Format code for both frontend and backend

## Project Structure

```
ai-job-application-copilot/
├── frontend/                 # Next.js frontend application
│   ├── src/
│   │   ├── app/             # App Router pages
│   │   ├── components/       # Reusable UI components
│   │   ├── lib/            # Utility functions and configurations
│   │   └── types/          # TypeScript type definitions
│   ├── public/              # Static assets
│   └── package.json
├── backend/                 # FastAPI backend application
│   ├── app/                # Application modules
│   │   ├── api/           # API route handlers
│   │   ├── core/           # Core application logic
│   │   ├── models/         # Database models
│   │   └── services/       # Business logic services
│   ├── database/           # Database configuration and migrations
│   ├── tests/              # Backend tests
│   └── main.py            # FastAPI application entry point
├── docs/                  # Documentation and specifications
├── scripts/               # Build and deployment scripts
└── docker-compose.yml      # Docker configuration
```

## Environment Variables

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=AI Job Application Copilot
```

### Backend (.env)
```env
DATABASE_URL=postgresql://user:password@localhost:5432/ai_job_copilot
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
CORS_ORIGINS=http://localhost:3000
SECRET_KEY=your_secret_key
```

## API Documentation

Once the backend is running, visit http://localhost:8000/docs for interactive API documentation.

## Contributing

1. Create a feature branch
2. Make your changes
3. Run tests and linting: `npm run test && npm run lint`
4. Commit your changes
5. Open a pull request

## License

MIT License - see LICENSE file for details.
