from fastapi import APIRouter

from app.api.v1.endpoints import users, resumes, job_descriptions, applications, fit_analysis, tailoring

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(resumes.router, prefix="/resumes", tags=["resumes"])
api_router.include_router(job_descriptions.router, prefix="/job-descriptions", tags=["job-descriptions"])
api_router.include_router(applications.router, prefix="/applications", tags=["applications"])
api_router.include_router(fit_analysis.router, prefix="/fit-analysis", tags=["fit-analysis"])
api_router.include_router(tailoring.router, prefix="/tailoring", tags=["tailoring"])
