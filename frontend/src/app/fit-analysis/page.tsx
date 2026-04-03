'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'

interface FitAnalysis {
  fit_score: number
  skills_analysis: {
    matched_skills: Array<{
      skill: string
      category: string
      resume_evidence: string
      jd_requirement: string
      match_strength: string
    }>
    missing_skills: Array<{
      skill: string
      category: string
      jd_requirement: string
      importance: string
      gap_reason: string
    }>
    partial_matches: Array<{
      skill: string
      category: string
      resume_evidence: string
      jd_requirement: string
      match_strength: string
    }>
  }
  experience_analysis: {
    level_alignment: string
    years_experience_match: string
    relevant_experience_highlights: Array<{
      experience: string
      relevance_score: number
      alignment_reason: string
    }>
    experience_gaps: Array<{
      gap: string
      impact: string
      suggestion: string
    }>
  }
  role_alignment: {
    overall_alignment: string
    alignment_score: number
    strengths: string[]
    concerns: string[]
    recommendations: string[]
  }
  education_analysis: {
    education_match: string
    degree_alignment: string
    field_relevance: string
    additional_education_needed: string[]
  }
}

interface FitReport {
  id: number
  resume: {
    id: number
    title: string
  }
  job_description: {
    id: number
    job_title: string
    company: string
  }
  overall_fit_score: number
  skills_match_score: number
  experience_match_score: number
  education_match_score: number
  matched_skills: any[]
  missing_skills: any[]
  role_alignment: any
  recommendations: string[]
  created_at: string
}

export default function FitAnalysisPage() {
  const [fitReports, setFitReports] = useState<FitReport[]>([])
  const [selectedReport, setSelectedReport] = useState<FitReport | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [activeTab, setActiveTab] = useState('overview')

  useEffect(() => {
    fetchFitReports()
  }, [])

  const fetchFitReports = async () => {
    try {
      const response = await fetch('/api/v1/fit-analysis/reports')
      if (!response.ok) {
        throw new Error('Failed to fetch fit reports')
      }
      const data = await response.json()
      setFitReports(data.fit_reports)
    } catch (err: any) {
      setError(err.message || 'An error occurred')
    } finally {
      setLoading(false)
    }
  }

  const fetchFitReport = async (reportId: number) => {
    try {
      const response = await fetch(`/api/v1/fit-analysis/reports/${reportId}`)
      if (!response.ok) {
        throw new Error('Failed to fetch fit report')
      }
      const data = await response.json()
      setSelectedReport(data)
    } catch (err: any) {
      setError(err.message || 'An error occurred')
    }
  }

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600'
    if (score >= 60) return 'text-yellow-600'
    return 'text-red-600'
  }

  const getScoreBgColor = (score: number) => {
    if (score >= 80) return 'bg-green-100'
    if (score >= 60) return 'bg-yellow-100'
    return 'bg-red-100'
  }

  const getAlignmentColor = (alignment: string) => {
    if (alignment === 'strong') return 'text-green-600'
    if (alignment === 'moderate') return 'text-yellow-600'
    return 'text-red-600'
  }

  if (loading) {
    return (
      <div className="container mx-auto px-4 py-8 max-w-6xl">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-r-2 border-t-2 border-l-2 border-primary-foreground mx-auto"></div>
          <p className="mt-4 text-muted-foreground">Loading fit analysis...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="container mx-auto px-4 py-8 max-w-6xl">
        <div className="text-center">
          <div className="bg-destructive/10 border border-destructive/20 text-destructive p-4 rounded-md">
            <p className="text-sm">{error}</p>
          </div>
          <button
            onClick={fetchFitReports}
            className="mt-4 inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-primary text-primary-foreground hover:bg-primary/90 h-10 px-4"
          >
            Try Again
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="container mx-auto px-4 py-8 max-w-6xl">
      <div className="mb-8">
        <h1 className="text-3xl font-bold tracking-tight text-foreground mb-2">
          Fit Analysis
        </h1>
        <p className="text-lg text-muted-foreground">
          Compare your resumes with job descriptions to see how well you match
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Fit Reports List */}
        <div className="lg:col-span-1">
          <div className="bg-card p-6 rounded-lg border">
            <h2 className="text-lg font-semibold text-foreground mb-4">
              Your Fit Reports
            </h2>
            
            {fitReports.length === 0 ? (
              <div className="text-center py-8">
                <p className="text-muted-foreground mb-4">
                  No fit reports yet. Upload resumes and job descriptions to get started.
                </p>
                <Link
                  href="/resume-upload"
                  className="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-primary text-primary-foreground hover:bg-primary/90 h-10 px-4"
                >
                  Upload Resume
                </Link>
              </div>
            ) : (
              <div className="space-y-3">
                {fitReports.map((report) => (
                  <div
                    key={report.id}
                    className={`p-4 border rounded-lg cursor-pointer transition-colors hover:bg-muted/50 ${
                      selectedReport?.id === report.id ? 'bg-muted border-primary' : ''
                    }`}
                    onClick={() => fetchFitReport(report.id)}
                  >
                    <div className="flex justify-between items-start mb-2">
                      <div>
                        <h3 className="font-semibold text-foreground text-sm">
                          {report.job_description?.job_title}
                        </h3>
                        <p className="text-xs text-muted-foreground">
                          {report.job_description?.company}
                        </p>
                      </div>
                      <div className={`text-right`}>
                        <div className={`text-lg font-bold ${getScoreColor(report.overall_fit_score)}`}>
                          {report.overall_fit_score}%
                        </div>
                        <div className="text-xs text-muted-foreground">
                          Fit Score
                        </div>
                      </div>
                    </div>
                    <div className="text-xs text-muted-foreground">
                      Resume: {report.resume?.title}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Fit Analysis Details */}
        <div className="lg:col-span-2">
          {selectedReport ? (
            <div className="bg-card p-6 rounded-lg border">
              <div className="mb-6">
                <h2 className="text-2xl font-bold text-foreground mb-2">
                  {selectedReport.job_description?.job_title}
                </h2>
                <p className="text-muted-foreground mb-4">
                  {selectedReport.job_description?.company}
                </p>
                
                {/* Overall Fit Score */}
                <div className="flex items-center justify-center mb-6">
                  <div className="text-center">
                    <div className={`text-6xl font-bold ${getScoreColor(selectedReport.overall_fit_score)}`}>
                      {selectedReport.overall_fit_score}%
                    </div>
                    <div className="text-sm text-muted-foreground">
                      Overall Fit Score
                    </div>
                  </div>
                </div>

                {/* Score Breakdown */}
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                  <div className="text-center">
                    <div className={`text-2xl font-bold ${getScoreColor(selectedReport.skills_match_score)}`}>
                      {selectedReport.skills_match_score}%
                    </div>
                    <div className="text-xs text-muted-foreground">Skills</div>
                  </div>
                  <div className="text-center">
                    <div className={`text-2xl font-bold ${getScoreColor(selectedReport.experience_match_score)}`}>
                      {selectedReport.experience_match_score}%
                    </div>
                    <div className="text-xs text-muted-foreground">Experience</div>
                  </div>
                  <div className="text-center">
                    <div className={`text-2xl font-bold ${getScoreColor(selectedReport.education_match_score)}`}>
                      {selectedReport.education_match_score}%
                    </div>
                    <div className="text-xs text-muted-foreground">Education</div>
                  </div>
                  <div className="text-center">
                    <div className={`text-lg font-bold ${getAlignmentColor(selectedReport.role_alignment?.overall_alignment || '')}`}>
                      {selectedReport.role_alignment?.overall_alignment || ''}
                    </div>
                    <div className="text-xs text-muted-foreground">Alignment</div>
                  </div>
                </div>

                {/* Tabs */}
                <div className="flex space-x-1 mb-6">
                  {['overview', 'skills', 'experience', 'recommendations'].map((tab) => (
                    <button
                      key={tab}
                      onClick={() => setActiveTab(tab)}
                      className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                        activeTab === tab
                          ? 'bg-primary text-primary-foreground'
                          : 'bg-secondary text-secondary-foreground hover:bg-secondary/80'
                      }`}
                    >
                      {tab.charAt(0).toUpperCase() + tab.slice(1)}
                    </button>
                  ))}
                </div>

                {/* Tab Content */}
                {activeTab === 'overview' && (
                  <div className="space-y-6">
                    {/* Strengths */}
                    <div>
                      <h3 className="text-lg font-semibold text-foreground mb-3">Strengths</h3>
                      <div className="space-y-2">
                        {selectedReport.role_alignment?.strengths?.map((strength, index) => (
                          <div key={index} className="flex items-center space-x-2">
                            <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                            <span className="text-sm">{strength}</span>
                          </div>
                        ))}
                      </div>
                    </div>

                    {/* Concerns */}
                    <div>
                      <h3 className="text-lg font-semibold text-foreground mb-3">Areas for Improvement</h3>
                      <div className="space-y-2">
                        {selectedReport.role_alignment?.concerns?.map((concern, index) => (
                          <div key={index} className="flex items-center space-x-2">
                            <div className="w-2 h-2 bg-yellow-500 rounded-full"></div>
                            <span className="text-sm">{concern}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                )}

                {activeTab === 'skills' && (
                  <div className="space-y-6">
                    {/* Matched Skills */}
                    <div>
                      <h3 className="text-lg font-semibold text-foreground mb-3">
                        Matched Skills ({selectedReport.matched_skills?.length || 0})
                      </h3>
                      <div className="space-y-2">
                        {selectedReport.matched_skills?.map((skill, index) => (
                          <div key={index} className={`p-3 rounded-lg ${getScoreBgColor(90)}`}>
                            <div className="flex justify-between items-start">
                              <div>
                                <h4 className="font-semibold text-sm">{skill.skill}</h4>
                                <p className="text-xs text-muted-foreground">{skill.category}</p>
                              </div>
                              <span className={`text-xs px-2 py-1 rounded ${skill.match_strength === 'strong' ? 'bg-green-200 text-green-800' : 'bg-yellow-200 text-yellow-800'}`}>
                                {skill.match_strength}
                              </span>
                            </div>
                            <p className="text-xs text-muted-foreground mt-1">{skill.resume_evidence}</p>
                          </div>
                        ))}
                      </div>
                    </div>

                    {/* Missing Skills */}
                    <div>
                      <h3 className="text-lg font-semibold text-foreground mb-3">
                        Missing Skills ({selectedReport.missing_skills?.length || 0})
                      </h3>
                      <div className="space-y-2">
                        {selectedReport.missing_skills?.map((skill, index) => (
                          <div key={index} className={`p-3 rounded-lg ${getScoreBgColor(30)}`}>
                            <div className="flex justify-between items-start">
                              <div>
                                <h4 className="font-semibold text-sm">{skill.skill}</h4>
                                <p className="text-xs text-muted-foreground">{skill.category}</p>
                              </div>
                              <span className={`text-xs px-2 py-1 rounded ${skill.importance === 'high' ? 'bg-red-200 text-red-800' : 'bg-yellow-200 text-yellow-800'}`}>
                                {skill.importance}
                              </span>
                            </div>
                            <p className="text-xs text-muted-foreground mt-1">{skill.gap_reason}</p>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                )}

                {activeTab === 'experience' && (
                  <div className="space-y-6">
                    <div>
                      <h3 className="text-lg font-semibold text-foreground mb-3">Experience Analysis</h3>
                      <div className="grid grid-cols-2 gap-4 mb-6">
                        <div>
                          <p className="text-sm text-muted-foreground">Level Alignment</p>
                          <p className={`font-semibold ${getAlignmentColor('aligned')}`}>Aligned</p>
                        </div>
                        <div>
                          <p className="text-sm text-muted-foreground">Years Experience</p>
                          <p className={`font-semibold ${getScoreColor(80)}`}>Sufficient</p>
                        </div>
                      </div>
                    </div>

                    <div>
                      <h3 className="text-lg font-semibold text-foreground mb-3">Relevant Experience</h3>
                      <div className="space-y-3">
                        {selectedReport.role_alignment?.strengths?.filter(s => 'experience' in s.toLowerCase()).map((strength, index) => (
                          <div key={index} className="p-3 bg-green-50 rounded-lg">
                            <p className="text-sm">{strength}</p>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                )}

                {activeTab === 'recommendations' && (
                  <div className="space-y-4">
                    <h3 className="text-lg font-semibold text-foreground mb-3">Recommendations</h3>
                    <div className="space-y-3">
                      {selectedReport.recommendations?.map((recommendation, index) => (
                        <div key={index} className="p-4 bg-blue-50 rounded-lg border border-blue-200">
                          <p className="text-sm">{recommendation}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          ) : (
            <div className="bg-card p-6 rounded-lg border">
              <div className="text-center py-12">
                <p className="text-muted-foreground mb-4">
                  Select a fit report from the list to view detailed analysis
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
