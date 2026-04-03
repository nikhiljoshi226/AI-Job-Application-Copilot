from fastapi import APIRouter

from app.api.v1.endpoints import users, resumes, job_descriptions, applications, fit_analysis, tailoring, tailored_resumes, exports, cover_letters, outreach_drafts, applications_tracker, interview_prep, skill_gap_analysis

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(resumes.router, prefix="/resumes", tags=["resumes"])
api_router.include_router(job_descriptions.router, prefix="/job-descriptions", tags=["job-descriptions"])
api_router.include_router(applications.router, prefix="/applications", tags=["applications"])
api_router.include_router(fit_analysis.router, prefix="/fit-analysis", tags=["fit-analysis"])
api_router.include_router(tailoring.router, prefix="/tailoring", tags=["tailoring"])
api_router.include_router(tailored_resumes.router, prefix="/tailored-resumes", tags=["tailored-resumes"])
api_router.include_router(exports.router, prefix="/exports", tags=["exports"])
api_router.include_router(cover_letters.router, prefix="/cover-letters", tags=["cover-letters"])
api_router.include_router(outreach_drafts.router, prefix="/outreach-drafts", tags=["outreach-drafts"])
api_router.include_router(applications_tracker.router, prefix="/applications-tracker", tags=["applications-tracker"])
api_router.include_router(interview_prep.router, prefix="/interview-prep", tags=["interview-prep"])
api_router.include_router(skill_gap_analysis.router, prefix="/skill-gap-analysis", tags=["skill-gap-analysis"])
