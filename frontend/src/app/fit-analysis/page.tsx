"use client"

import { AppLayout } from '@/components/layout/app-layout'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { 
  Target, 
  CheckCircle, 
  XCircle, 
  AlertTriangle,
  TrendingUp,
  ArrowRight,
  Download,
  Share
} from 'lucide-react'

// Mock data
const fitAnalysisData = {
  analysisName: "Senior Frontend Developer at TechCorp",
  overallScore: 85,
  status: "completed",
  analyzedAt: "2024-01-15T10:30:00Z",
  resume: {
    title: "Senior Frontend Developer Resume",
    fileName: "john_doe_frontend_dev.pdf"
  },
  jobDescription: {
    title: "Senior Frontend Developer",
    company: "TechCorp",
    location: "San Francisco, CA"
  },
  matchedSkills: [
    {
      name: "React",
      category: "Framework",
      experience: "5 years",
      proficiency: "Expert"
    },
    {
      name: "TypeScript",
      category: "Language",
      experience: "4 years",
      proficiency: "Advanced"
    },
    {
      name: "Node.js",
      category: "Backend",
      experience: "3 years",
      proficiency: "Intermediate"
    },
    {
      name: "CSS/Tailwind",
      category: "Styling",
      experience: "5 years",
      proficiency: "Expert"
    },
    {
      name: "Git",
      category: "Tool",
      experience: "5 years",
      proficiency: "Expert"
    }
  ],
  missingSkills: [
    {
      name: "GraphQL",
      category: "Technology",
      importance: "High",
      mentionedInJD: true
    },
    {
      name: "AWS",
      category: "Cloud Platform",
      importance: "Medium",
      mentionedInJD: true
    },
    {
      name: "Docker",
      category: "DevOps",
      importance: "Medium",
      mentionedInJD: true
    }
  ],
  relevantExperience: [
    {
      title: "Senior Frontend Developer",
      company: "Current Company",
      duration: "2 years",
      relevance: "High",
      description: "Led development of enterprise React applications"
    },
    {
      title: "Full Stack Developer",
      company: "Previous Company",
      duration: "3 years",
      relevance: "High",
      description: "Built full-stack web applications using React and Node.js"
    }
  ],
  unsupportedRequirements: [
    {
      requirement: "GraphQL experience",
      reason: "Not found in resume or experience"
    },
    {
      requirement: "Cloud deployment experience",
      reason: "No cloud platform experience listed"
    }
  ]
}

const getScoreColor = (score: number) => {
  if (score >= 80) return "text-green-600"
  if (score >= 60) return "text-yellow-600"
  return "text-red-600"
}

const getScoreBadge = (score: number) => {
  if (score >= 80) return { variant: "default" as const, text: "Excellent Fit" }
  if (score >= 60) return { variant: "secondary" as const, text: "Good Fit" }
  return { variant: "destructive" as const, text: "Poor Fit" }
}

export default function FitAnalysisPage() {
  const scoreBadge = getScoreBadge(fitAnalysisData.overallScore)
  const scoreColor = getScoreColor(fitAnalysisData.overallScore)

  return (
    <AppLayout>
      <div className="max-w-6xl mx-auto space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold tracking-tight">Fit Analysis Results</h1>
            <p className="text-muted-foreground">
              Analysis of your resume against the job description
            </p>
          </div>
          <div className="flex space-x-2">
            <Button variant="outline">
              <Download className="mr-2 h-4 w-4" />
              Export PDF
            </Button>
            <Button variant="outline">
              <Share className="mr-2 h-4 w-4" />
              Share
            </Button>
          </div>
        </div>

        {/* Overview Card */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <Target className="mr-2 h-5 w-5" />
              Analysis Overview
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
              {/* Overall Score */}
              <div className="text-center">
                <div className={`text-4xl font-bold ${scoreColor}`}>
                  {fitAnalysisData.overallScore}%
                </div>
                <Badge variant={scoreBadge.variant} className="mt-2">
                  {scoreBadge.text}
                </Badge>
                <p className="text-sm text-muted-foreground mt-2">
                  Overall Fit Score
                </p>
              </div>

              {/* Resume Info */}
              <div>
                <h4 className="font-medium mb-2">Resume</h4>
                <p className="text-sm text-muted-foreground">
                  {fitAnalysisData.resume.title}
                </p>
                <p className="text-xs text-muted-foreground">
                  {fitAnalysisData.resume.fileName}
                </p>
              </div>

              {/* Job Info */}
              <div>
                <h4 className="font-medium mb-2">Job Description</h4>
                <p className="text-sm text-muted-foreground">
                  {fitAnalysisData.jobDescription.title}
                </p>
                <p className="text-xs text-muted-foreground">
                  {fitAnalysisData.jobDescription.company} • {fitAnalysisData.jobDescription.location}
                </p>
              </div>

              {/* Analysis Date */}
              <div>
                <h4 className="font-medium mb-2">Analyzed</h4>
                <p className="text-sm text-muted-foreground">
                  {new Date(fitAnalysisData.analyzedAt).toLocaleDateString()}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        <div className="grid gap-6 lg:grid-cols-2">
          {/* Matched Skills */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center text-green-600">
                <CheckCircle className="mr-2 h-5 w-5" />
                Matched Skills
              </CardTitle>
              <CardDescription>
                Skills from your resume that match the job requirements
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {fitAnalysisData.matchedSkills.map((skill, index) => (
                  <div key={index} className="flex items-center justify-between p-3 border rounded-lg">
                    <div>
                      <h5 className="font-medium">{skill.name}</h5>
                      <div className="flex items-center space-x-2 text-sm text-muted-foreground">
                        <span>{skill.category}</span>
                        <span>•</span>
                        <span>{skill.experience}</span>
                        <span>•</span>
                        <span>{skill.proficiency}</span>
                      </div>
                    </div>
                    <CheckCircle className="h-4 w-4 text-green-600" />
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Missing Skills */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center text-red-600">
                <XCircle className="mr-2 h-5 w-5" />
                Missing Skills
              </CardTitle>
              <CardDescription>
                Skills required by the job that are not in your resume
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {fitAnalysisData.missingSkills.map((skill, index) => (
                  <div key={index} className="flex items-center justify-between p-3 border rounded-lg">
                    <div>
                      <h5 className="font-medium">{skill.name}</h5>
                      <div className="flex items-center space-x-2 text-sm text-muted-foreground">
                        <span>{skill.category}</span>
                        <span>•</span>
                        <Badge variant={skill.importance === "High" ? "destructive" : "secondary"}>
                          {skill.importance} Priority
                        </Badge>
                      </div>
                    </div>
                    <XCircle className="h-4 w-4 text-red-600" />
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Relevant Experience */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <TrendingUp className="mr-2 h-5 w-5" />
              Relevant Experience
            </CardTitle>
            <CardDescription>
              Your experience that aligns with this role
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {fitAnalysisData.relevantExperience.map((exp, index) => (
                <div key={index} className="p-4 border rounded-lg">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <h5 className="font-medium">{exp.title}</h5>
                      <p className="text-sm text-muted-foreground mb-2">
                        {exp.company} • {exp.duration}
                      </p>
                      <p className="text-sm">{exp.description}</p>
                    </div>
                    <Badge variant={exp.relevance === "High" ? "default" : "secondary"}>
                      {exp.relevance} Relevance
                    </Badge>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Unsupported Requirements */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center text-orange-600">
              <AlertTriangle className="mr-2 h-5 w-5" />
              Unsupported Requirements
            </CardTitle>
            <CardDescription>
              Job requirements that couldn't be matched to your profile
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {fitAnalysisData.unsupportedRequirements.map((req, index) => (
                <div key={index} className="p-3 border rounded-lg bg-orange-50 border-orange-200">
                  <div className="flex items-start">
                    <AlertTriangle className="h-4 w-4 text-orange-600 mr-2 mt-0.5" />
                    <div>
                      <h5 className="font-medium text-orange-800">{req.requirement}</h5>
                      <p className="text-sm text-orange-600">{req.reason}</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Action Buttons */}
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <div>
                <h4 className="font-medium">Next Steps</h4>
                <p className="text-sm text-muted-foreground">
                  Get tailored suggestions to improve your fit
                </p>
              </div>
              <Button>
                <ArrowRight className="mr-2 h-4 w-4" />
                Go to Tailoring Review
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </AppLayout>
  )
}
