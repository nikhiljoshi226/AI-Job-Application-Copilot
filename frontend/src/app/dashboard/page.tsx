'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'

interface Resume {
  id: number
  title: string
  file_name: string
  file_type: string
  is_active: string
  created_at: string
  updated_at: string
  text_length: number
}

interface DashboardData {
  resumes: Resume[]
  total: number
}

export default function DashboardPage() {
  const [dashboardData, setDashboardData] = useState<DashboardData | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    fetchResumes()
  }, [])

  const fetchResumes = async () => {
    try {
      const response = await fetch('/api/v1/resumes')
      if (!response.ok) {
        throw new Error('Failed to fetch resumes')
      }
      const data = await response.json()
      setDashboardData(data)
    } catch (err: any) {
      setError(err.message || 'An error occurred')
    } finally {
      setLoading(false)
    }
  }

  const getStatusBadge = (status: string) => {
    const statusStyles = {
      draft: 'bg-yellow-100 text-yellow-800',
      active: 'bg-green-100 text-green-800',
      archived: 'bg-gray-100 text-gray-800'
    }
    return (
      <span className={`px-2 py-1 rounded-full text-xs font-medium ${statusStyles[status as keyof typeof statusStyles] || statusStyles.draft}`}>
        {status}
      </span>
    )
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString()
  }

  if (loading) {
    return (
      <div className="container mx-auto px-4 py-8 max-w-4xl">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-r-2 border-t-2 border-l-2 border-primary-foreground mx-auto"></div>
          <p className="mt-4 text-muted-foreground">Loading your resumes...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="container mx-auto px-4 py-8 max-w-4xl">
        <div className="text-center">
          <div className="bg-destructive/10 border border-destructive/20 text-destructive p-4 rounded-md">
            <p className="text-sm">{error}</p>
          </div>
          <button
            onClick={fetchResumes}
            className="mt-4 inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-primary text-primary-foreground hover:bg-primary/90 h-10 px-4"
          >
            Try Again
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="container mx-auto px-4 py-8 max-w-4xl">
      <div className="mb-8">
        <h1 className="text-3xl font-bold tracking-tight text-foreground mb-2">
          Dashboard
        </h1>
        <p className="text-lg text-muted-foreground">
          Manage your resumes and job applications
        </p>
      </div>

      {dashboardData && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Stats Cards */}
          <div className="lg:col-span-3">
            <div className="bg-card p-6 rounded-lg border">
              <h3 className="text-lg font-semibold text-foreground mb-4">
                Your Resumes
              </h3>
              <div className="text-3xl font-bold text-primary">
                {dashboardData.total}
              </div>
              <p className="text-sm text-muted-foreground">
                Total resumes uploaded
              </p>
            </div>
          </div>

          {/* Quick Actions */}
          <div className="lg:col-span-3">
            <div className="bg-card p-6 rounded-lg border">
              <h3 className="text-lg font-semibold text-foreground mb-4">
                Quick Actions
              </h3>
              <div className="space-y-3">
                <Link
                  href="/resume-upload"
                  className="block w-full text-center inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-primary text-primary-foreground hover:bg-primary/90 h-10 px-4"
                >
                  Upload New Resume
                </Link>
                <Link
                  href="/job-analysis"
                  className="block w-full text-center inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-secondary text-secondary-foreground hover:bg-secondary/80 h-10 px-4"
                >
                  Analyze Job Description
                </Link>
              </div>
            </div>
          </div>

          {/* Recent Activity */}
          <div className="lg:col-span-3">
            <div className="bg-card p-6 rounded-lg border">
              <h3 className="text-lg font-semibold text-foreground mb-4">
                Recent Activity
              </h3>
              <div className="text-sm text-muted-foreground">
                <p>Your most recent resume was uploaded on {dashboardData.resumes[0] ? formatDate(dashboardData.resumes[0].created_at) : 'N/A'}</p>
              </div>
            </div>
          </div>
        </div>

        {/* Resumes List */}
        <div className="lg:col-span-3">
          <div className="bg-card p-6 rounded-lg border">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-lg font-semibold text-foreground">
                Your Resumes
              </h3>
              <Link
                href="/resume-upload"
                className="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-primary text-primary-foreground hover:bg-primary/90 h-8 px-3"
              >
                Add New
              </Link>
            </div>

            {dashboardData.resumes.length === 0 ? (
              <div className="text-center py-8">
                <p className="text-muted-foreground mb-4">
                  You haven't uploaded any resumes yet.
                </p>
                <Link
                  href="/resume-upload"
                  className="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-primary text-primary-foreground hover:bg-primary/90 h-10 px-4"
                >
                  Upload Your First Resume
                </Link>
              </div>
            ) : (
              <div className="space-y-4">
                {dashboardData.resumes.map((resume) => (
                  <div key={resume.id} className="border rounded-lg p-4 hover:bg-muted/50 transition-colors">
                    <div className="flex justify-between items-start mb-2">
                      <div>
                        <h4 className="font-semibold text-foreground">
                          {resume.title}
                        </h4>
                        <p className="text-sm text-muted-foreground">
                          {resume.file_name} • {resume.text_length} characters
                        </p>
                      </div>
                      <div className="flex items-center space-x-2">
                        {getStatusBadge(resume.is_active)}
                        <span className="text-xs text-muted-foreground">
                          {formatDate(resume.created_at)}
                        </span>
                      </div>
                    </div>
                    <div className="text-sm text-muted-foreground">
                      Last updated: {formatDate(resume.updated_at)}
                    </div>
                    <div className="flex space-x-2 mt-3">
                      <button className="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-secondary text-secondary-foreground hover:bg-secondary/80 h-8 px-3">
                        View
                      </button>
                      <button className="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-primary text-primary-foreground hover:bg-primary/90 h-8 px-3">
                        Use for Application
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}
