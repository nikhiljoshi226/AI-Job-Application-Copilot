"use client"

import { useState } from 'react'
import { AppLayout } from '@/components/layout/app-layout'
import { 
  Upload, 
  FileText, 
  Target,
  Plus,
  X,
  CheckCircle2,
  AlertCircle,
  Calendar,
  Clock,
  Briefcase
} from 'lucide-react'

// Mock data
const mockResumes = [
  {
    id: 1,
    title: "Senior Frontend Developer Resume",
    fileName: "john_doe_frontend_dev.pdf",
    uploadedDate: "2024-01-15",
    status: "active",
    lastUsed: "2 days ago",
    fitScore: 85
  },
  {
    id: 2,
    title: "Full Stack Developer Resume",
    fileName: "john_doe_full_stack.pdf",
    uploadedDate: "2024-01-10",
    status: "active",
    lastUsed: "1 week ago",
    fitScore: 72
  },
  {
    id: 3,
    title: "Software Engineer Resume",
    fileName: "john_doe_software_eng.pdf",
    uploadedDate: "2024-01-05",
    status: "archived",
    lastUsed: "2 weeks ago",
    fitScore: 68
  }
]

export default function InputBootstrapPage() {
  const [selectedResume, setSelectedResume] = useState<number | null>(null)
  const [jobDescription, setJobDescription] = useState('')
  const [analysisName, setAnalysisName] = useState('')
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [uploadedFile, setUploadedFile] = useState<File | null>(null)

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (file) {
      setUploadedFile(file)
    }
  }

  const handleAnalyze = async () => {
    if (!selectedResume && !uploadedFile) {
      alert('Please select or upload a resume')
      return
    }
    if (!jobDescription.trim()) {
      alert('Please enter a job description')
      return
    }

    setIsAnalyzing(true)
    setTimeout(() => {
      setIsAnalyzing(false)
      window.location.href = '/fit-analysis'
    }, 2000)
  }

  const removeUploadedFile = () => {
    setUploadedFile(null)
  }

  const getScoreColor = (score: number) => {
    if (score >= 80) return "success"
    if (score >= 60) return "warning"
    return "danger"
  }

  const getStatusBadge = (status: string) => {
    const variants = {
      active: "primary",
      archived: "secondary"
    }
    return variants[status as keyof typeof variants] || "secondary"
  }

  return (
    <AppLayout>
      <div className="container-fluid py-4">
        {/* Header */}
        <div className="text-center mb-5">
          <div className="d-inline-flex align-items-center px-3 py-2 bg-primary text-white rounded-pill mb-3">
            <span className="me-2">⚡</span>
            AI-Powered Job Matching
          </div>
          <h1 className="display-4 fw-bold text-primary mb-3">Find Your Perfect Match</h1>
          <p className="lead text-muted mx-auto" style={{maxWidth: '600px'}}>
            Upload your resume and paste the job description to get instant AI-powered compatibility analysis with personalized recommendations.
          </p>
        </div>

        {/* Quick Stats */}
        <div className="row mb-5">
          <div className="col-md-4 mb-3">
            <div className="card border-0 shadow-sm">
              <div className="card-body">
                <div className="d-flex align-items-center">
                  <div className="p-2 bg-primary bg-opacity-10 rounded me-3">
                    <FileText className="text-primary" size={20} />
                  </div>
                  <div>
                    <p className="text-muted small mb-0">Total Resumes</p>
                    <p className="h4 mb-0 fw-bold">12</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div className="col-md-4 mb-3">
            <div className="card border-0 shadow-sm">
              <div className="card-body">
                <div className="d-flex align-items-center">
                  <div className="p-2 bg-success bg-opacity-10 rounded me-3">
                    <Target className="text-success" size={20} />
                  </div>
                  <div>
                    <p className="text-muted small mb-0">Analyses Completed</p>
                    <p className="h4 mb-0 fw-bold">48</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div className="col-md-4 mb-3">
            <div className="card border-0 shadow-sm">
              <div className="card-body">
                <div className="d-flex align-items-center">
                  <div className="p-2 bg-warning bg-opacity-10 rounded me-3">
                    <span className="text-warning fw-bold">⚡</span>
                  </div>
                  <div>
                    <p className="text-muted small mb-0">Avg. Fit Score</p>
                    <p className="h4 mb-0 fw-bold">78%</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="row">
          {/* Resume Selection */}
          <div className="col-lg-6 mb-4">
            <div className="card border-0 shadow">
              <div className="card-header bg-primary text-white">
                <h5 className="mb-0 d-flex align-items-center">
                  <FileText className="me-2" size={20} />
                  Select Your Resume
                </h5>
              </div>
              <div className="card-body">
                {/* Existing Resumes */}
                <div className="mb-4">
                  <h6 className="fw-bold mb-3 d-flex align-items-center">
                    <Briefcase className="me-2 text-primary" size={16} />
                    Your Resumes
                  </h6>
                  {mockResumes.map((resume) => (
                    <div
                      key={resume.id}
                      className={`card mb-3 cursor-pointer transition-all ${
                        selectedResume === resume.id
                          ? 'border-primary bg-light'
                          : 'border-secondary hover:border-primary'
                      }`}
                      onClick={() => setSelectedResume(resume.id)}
                    >
                      <div className="card-body">
                        <div className="d-flex align-items-start justify-content-between">
                          <div className="flex-grow-1">
                            <div className="d-flex align-items-center mb-2">
                              <h6 className="fw-bold mb-0">{resume.title}</h6>
                              {selectedResume === resume.id && (
                                <CheckCircle2 className="ms-2 text-primary" size={16} />
                              )}
                            </div>
                            <div className="d-flex align-items-center text-muted small mb-2">
                              <FileText className="me-1" size={14} />
                              <span>{resume.fileName}</span>
                              <span className="mx-2">•</span>
                              <Calendar className="me-1" size={14} />
                              <span>Uploaded {resume.uploadedDate}</span>
                            </div>
                            <div className="d-flex flex-wrap gap-2">
                              <span className={`badge bg-${getStatusBadge(resume.status)} text-white`}>
                                {resume.status}
                              </span>
                              <span className="badge bg-light text-dark">
                                <Clock className="me-1" size={12} />
                                Used {resume.lastUsed}
                              </span>
                              <span className={`badge bg-${getScoreColor(resume.fitScore)} text-white`}>
                                <Target className="me-1" size={12} />
                                {resume.fitScore}% match
                              </span>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>

                {/* Upload Section */}
                <div className="border-top pt-4">
                  <h6 className="fw-bold mb-3 d-flex align-items-center">
                    <Plus className="me-2 text-primary" size={16} />
                    Upload New Resume
                  </h6>
                  {uploadedFile ? (
                    <div className="alert alert-success d-flex align-items-center justify-content-between">
                      <div className="d-flex align-items-center">
                        <FileText className="me-2 text-success" size={16} />
                        <div>
                          <div className="fw-medium">{uploadedFile.name}</div>
                          <small className="text-muted">
                            ({(uploadedFile.size / 1024).toFixed(1)} KB)
                          </small>
                        </div>
                      </div>
                      <button
                        className="btn btn-sm btn-outline-danger"
                        onClick={removeUploadedFile}
                      >
                        <X size={16} />
                      </button>
                    </div>
                  ) : (
                    <div className="border-2 border-dashed border-secondary rounded p-4 text-center">
                      <div className="mb-3">
                        <Upload className="text-muted" size={32} />
                      </div>
                      <p className="mb-2">Drop your resume here</p>
                      <p className="text-muted small mb-3">or click to browse files</p>
                      <p className="text-muted small mb-3">PDF, DOC, DOCX (Max 10MB)</p>
                      <input
                        type="file"
                        accept=".pdf,.doc,.docx"
                        onChange={handleFileUpload}
                        className="d-none"
                        id="resume-upload"
                      />
                      <label htmlFor="resume-upload" className="btn btn-primary">
                        Choose File
                      </label>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>

          {/* Job Description Input */}
          <div className="col-lg-6 mb-4">
            <div className="card border-0 shadow">
              <div className="card-header bg-success text-white">
                <h5 className="mb-0 d-flex align-items-center">
                  <Target className="me-2" size={20} />
                  Job Description
                </h5>
              </div>
              <div className="card-body">
                {/* Analysis Name */}
                <div className="mb-4">
                  <label htmlFor="analysis-name" className="form-label fw-semibold">
                    Analysis Name <small className="text-muted">(Optional)</small>
                  </label>
                  <input
                    type="text"
                    className="form-control"
                    id="analysis-name"
                    placeholder="e.g., Senior Frontend Developer at TechCorp"
                    value={analysisName}
                    onChange={(e) => setAnalysisName(e.target.value)}
                  />
                </div>

                {/* Job Description */}
                <div className="mb-4">
                  <label htmlFor="job-description" className="form-label fw-semibold">
                    Job Description <span className="text-danger">*</span>
                  </label>
                  <textarea
                    className="form-control"
                    id="job-description"
                    rows={8}
                    placeholder="Paste the complete job description here... Include requirements, responsibilities, and qualifications for the best analysis results."
                    value={jobDescription}
                    onChange={(e) => setJobDescription(e.target.value)}
                  ></textarea>
                  <div className="d-flex justify-content-between mt-2">
                    <small className="text-muted">
                      {jobDescription.length} characters
                    </small>
                    {jobDescription.length > 0 && (
                      <small className="text-success">
                        <CheckCircle2 className="me-1" size={12} />
                        Ready for analysis
                      </small>
                    )}
                  </div>
                </div>

                {/* Tips */}
                <div className="alert alert-info">
                  <h6 className="alert-heading fw-bold mb-2">
                    <span className="me-2">ℹ️</span>
                    Pro Tips for Best Results:
                  </h6>
                  <ul className="mb-0 small">
                    <li>Include the complete job description with all requirements</li>
                    <li>Ensure your resume is up-to-date with recent experience</li>
                    <li>The AI will identify skill gaps and provide tailored recommendations</li>
                    <li>Results include compatibility score and improvement suggestions</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Analysis Button */}
        <div className="card border-0 shadow bg-gradient">
          <div className="card-body">
            <div className="d-flex align-items-center justify-content-between">
              <div>
                <h4 className="fw-bold mb-2">Ready to Analyze?</h4>
                <div className="d-flex align-items-center gap-3">
                  <div className="d-flex align-items-center">
                    {selectedResume || uploadedFile ? (
                      <>
                        <CheckCircle2 className="me-2 text-success" size={16} />
                        <span>Resume selected</span>
                      </>
                    ) : (
                      <>
                        <AlertCircle className="me-2 text-warning" size={16} />
                        <span>No resume selected</span>
                      </>
                    )}
                  </div>
                  <span>•</span>
                  <div className="d-flex align-items-center">
                    {jobDescription.trim() ? (
                      <>
                        <CheckCircle2 className="me-2 text-success" size={16} />
                        <span>Job description provided</span>
                      </>
                    ) : (
                      <>
                        <AlertCircle className="me-2 text-warning" size={16} />
                        <span>No job description</span>
                      </>
                    )}
                  </div>
                </div>
              </div>
              <button
                className="btn btn-light btn-lg px-4"
                onClick={handleAnalyze}
                disabled={isAnalyzing || (!selectedResume && !uploadedFile) || !jobDescription.trim()}
              >
                {isAnalyzing ? (
                  <>
                    <div className="spinner-border spinner-border-sm me-2" role="status">
                      <span className="visually-hidden">Loading...</span>
                    </div>
                    Analyzing...
                  </>
                ) : (
                  <>
                    <Target className="me-2" size={20} />
                    Start Analysis
                  </>
                )}
              </button>
            </div>
          </div>
        </div>
      </div>
    </AppLayout>
  )
}
