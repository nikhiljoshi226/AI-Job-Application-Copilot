"use client"

import { AppLayout } from '@/components/layout/app-layout'
import { 
  FileText, 
  Target, 
  TrendingUp, 
  Calendar,
  Briefcase,
  BarChart3,
  Clock,
  CheckCircle2,
  Star,
  Zap
} from 'lucide-react'

// Mock data
const recentAnalyses = [
  {
    id: 1,
    name: "Senior Frontend Developer at TechCorp",
    type: "Fit Analysis",
    score: 85,
    date: "2024-01-15",
    status: "completed",
    company: "TechCorp",
    location: "San Francisco, CA"
  },
  {
    id: 2,
    name: "Full Stack Engineer at StartupXYZ",
    type: "Fit Analysis", 
    score: 72,
    date: "2024-01-14",
    status: "completed",
    company: "StartupXYZ",
    location: "Remote"
  },
  {
    id: 3,
    name: "React Developer at DigitalAgency",
    type: "Tailoring Review",
    score: null,
    date: "2024-01-13",
    status: "in_progress",
    company: "DigitalAgency",
    location: "New York, NY"
  }
]

const quickStats = [
  {
    title: "Total Analyses",
    value: "24",
    change: "+3 this week",
    icon: Target,
    color: "primary"
  },
  {
    title: "Avg. Fit Score",
    value: "78%",
    change: "+5% improvement",
    icon: TrendingUp,
    color: "success"
  },
  {
    title: "Resumes Uploaded",
    value: "12",
    change: "+2 this month",
    icon: FileText,
    color: "info"
  },
  {
    title: "Applications Sent",
    value: "8",
    change: "+1 this week",
    icon: Briefcase,
    color: "warning"
  }
]

const quickActions = [
  {
    title: "Upload New Resume",
    description: "Add a new resume to analyze",
    icon: FileText,
    color: "primary"
  },
  {
    title: "Analyze Job Description",
    description: "Check compatibility with your resume",
    icon: Target,
    color: "success"
  },
  {
    title: "Track Applications",
    description: "Monitor your job application status",
    icon: Briefcase,
    color: "info"
  },
  {
    title: "Skill Gap Analysis",
    description: "Identify areas for improvement",
    icon: TrendingUp,
    color: "warning"
  }
]

const getScoreColor = (score: number) => {
  if (score >= 80) return "success"
  if (score >= 60) return "warning"
  return "danger"
}

const getStatusBadge = (status: string) => {
  const variants = {
    completed: "success",
    in_progress: "warning",
    pending: "secondary"
  }
  return variants[status as keyof typeof variants] || "secondary"
}

export default function DashboardBootstrapPage() {
  return (
    <AppLayout>
      <div className="container-fluid py-4">
        {/* Header */}
        <div className="text-center mb-5">
          <div className="d-inline-flex align-items-center px-3 py-2 bg-primary text-white rounded-pill mb-3">
            <span className="me-2">⚡</span>
            Welcome Back!
          </div>
          <h1 className="display-4 fw-bold text-primary mb-3">Your Job Search Dashboard</h1>
          <p className="lead text-muted mx-auto" style={{maxWidth: '600px'}}>
            Track your job applications, analyze fit scores, and get AI-powered recommendations to land your dream job.
          </p>
        </div>

        {/* Quick Stats */}
        <div className="row mb-5">
          {quickStats.map((stat, index) => {
            const Icon = stat.icon
            return (
              <div key={index} className="col-lg-3 col-md-6 mb-3">
                <div className="card border-0 shadow-sm h-100">
                  <div className="card-body">
                    <div className="d-flex align-items-center justify-content-between mb-3">
                      <div className={`p-3 bg-${stat.color} bg-opacity-10 rounded`}>
                        <Icon className={`text-${stat.color}`} size={24} />
                      </div>
                      <div className="text-end">
                        <small className={`text-${stat.color} fw-medium`}>{stat.change}</small>
                      </div>
                    </div>
                    <div>
                      <h3 className="h2 mb-1 fw-bold">{stat.value}</h3>
                      <p className="text-muted small mb-0">{stat.title}</p>
                    </div>
                  </div>
                </div>
              </div>
            )
          })}
        </div>

        {/* Quick Actions */}
        <div className="mb-5">
          <h2 className="h4 fw-bold mb-4 d-flex align-items-center">
            <Zap className="me-2 text-warning" size={20} />
            Quick Actions
          </h2>
          <div className="row">
            {quickActions.map((action, index) => {
              const Icon = action.icon
              return (
                <div key={index} className="col-lg-3 col-md-6 mb-3">
                  <div className="card border-0 shadow-sm h-100">
                    <div className="card-body text-center">
                      <div className={`p-3 bg-${action.color} bg-opacity-10 rounded-circle d-inline-flex mb-3`}>
                        <Icon className={`text-${action.color}`} size={24} />
                      </div>
                      <h6 className="fw-bold mb-2">{action.title}</h6>
                      <p className="text-muted small mb-3">{action.description}</p>
                      <button className={`btn btn-${action.color} w-100`}>
                        Get Started
                        <span className="ms-2">→</span>
                      </button>
                    </div>
                  </div>
                </div>
              )
            })}
          </div>
        </div>

        {/* Recent Analyses */}
        <div className="mb-5">
          <div className="d-flex align-items-center justify-content-between mb-4">
            <h2 className="h4 fw-bold mb-0 d-flex align-items-center">
              <BarChart3 className="me-2 text-primary" size={20} />
              Recent Analyses
            </h2>
            <button className="btn btn-outline-secondary">
              View All
              <span className="ms-2">→</span>
            </button>
          </div>
          <div className="space-y-3">
            {recentAnalyses.map((analysis) => (
              <div key={analysis.id} className="card border-0 shadow-sm">
                <div className="card-body">
                  <div className="d-flex align-items-center justify-content-between">
                    <div className="flex-grow-1">
                      <div className="d-flex align-items-center mb-2">
                        <h6 className="fw-bold mb-0 me-3">{analysis.name}</h6>
                        <span className={`badge bg-${getStatusBadge(analysis.status)} text-white`}>
                          {analysis.status === 'completed' ? 'Completed' : analysis.status === 'in_progress' ? 'In Progress' : 'Pending'}
                        </span>
                      </div>
                      <div className="d-flex align-items-center text-muted small mb-2">
                        <Briefcase className="me-1" size={14} />
                        <span className="me-3">{analysis.company}</span>
                        <Calendar className="me-1" size={14} />
                        <span className="me-3">{analysis.date}</span>
                        <span className="me-3">•</span>
                        <span>{analysis.location}</span>
                      </div>
                      <div className="d-flex align-items-center gap-3">
                        <span className="badge bg-light text-dark">
                          {analysis.type}
                        </span>
                        {analysis.score && (
                          <div className="d-flex align-items-center">
                            <span className="text-muted small me-2">Fit Score:</span>
                            <span className={`badge bg-${getScoreColor(analysis.score)} text-white`}>
                              {analysis.score}%
                            </span>
                          </div>
                        )}
                      </div>
                    </div>
                    <div className="ms-3">
                      {analysis.status === "completed" && (
                        <button className="btn btn-primary btn-sm">
                          View Results
                          <span className="ms-2">→</span>
                        </button>
                      )}
                      {analysis.status === "in_progress" && (
                        <button className="btn btn-outline-warning btn-sm">
                          <Clock className="me-1" size={14} />
                          In Progress
                        </button>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Achievement Section */}
        <div className="card border-0 shadow bg-gradient bg-primary text-white">
          <div className="card-body">
            <div className="d-flex align-items-center justify-content-between">
              <div>
                <h2 className="h4 fw-bold mb-3 d-flex align-items-center">
                  <Star className="me-2" size={24} />
                  You're Doing Great!
                </h2>
                <p className="mb-3">
                  Your average fit score of 78% puts you in the top 25% of candidates. Keep up the excellent work!
                </p>
                <div className="d-flex align-items-center gap-4">
                  <div className="d-flex align-items-center">
                    <CheckCircle2 className="me-2" size={20} />
                    <span>24 Analyses Completed</span>
                  </div>
                  <div className="d-flex align-items-center">
                    <TrendingUp className="me-2" size={20} />
                    <span>5% Score Improvement</span>
                  </div>
                </div>
              </div>
              <div className="text-center">
                <div className="display-4 fw-bold mb-2">78%</div>
                <p className="mb-0">Avg. Fit Score</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </AppLayout>
  )
}
