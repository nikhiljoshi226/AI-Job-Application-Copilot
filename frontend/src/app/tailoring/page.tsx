"use client"

import { useState } from 'react'
import { AppLayout } from '@/components/layout/app-layout'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Textarea } from '@/components/ui/textarea'
import { 
  Edit3, 
  CheckCircle, 
  X, 
  Plus,
  Eye,
  Download,
  RefreshCw,
  AlertCircle,
  Lightbulb
} from 'lucide-react'

// Mock data
const tailoringSuggestions = [
  {
    id: 1,
    type: "skill_highlight",
    title: "Add GraphQL Experience",
    original: "Experience with REST APIs",
    suggested: "Experience with REST APIs and GraphQL",
    reason: "Job requires GraphQL knowledge",
    confidence: 0.85,
    evidence: {
      resume_snippet: "Built REST APIs for various projects",
      jd_requirement: "GraphQL experience required",
      improvement: "Add GraphQL projects to portfolio"
    },
    status: "pending"
  },
  {
    id: 2,
    type: "experience_reword",
    title: "Expand Cloud Deployment Experience",
    original: "Deployed applications to local servers",
    suggested: "Deployed applications to AWS cloud infrastructure",
    reason: "Job requires cloud deployment experience",
    confidence: 0.92,
    evidence: {
      resume_snippet: "Local deployment and testing",
      jd_requirement: "Cloud deployment experience",
      improvement: "Highlight AWS deployment projects"
    },
    status: "pending"
  },
  {
    id: 3,
    type: "skill_addition",
    title: "Add Docker Experience",
    original: "Manual deployment processes",
    suggested: "Containerized applications using Docker for deployment",
    reason: "Modern development practices require containerization",
    confidence: 0.78,
    evidence: {
      resume_snippet: "Manual deployment and configuration",
      jd_requirement: "Docker experience preferred",
      improvement: "Add Docker containerization projects"
    },
    status: "accepted"
  },
  {
    id: 4,
    type: "certification_suggestion",
    title: "Add AWS Certification",
    original: "Self-taught cloud skills",
    suggested: "AWS Certified Solutions Architect - Professional",
    reason: "Formal certification strengthens cloud credentials",
    confidence: 0.70,
    evidence: {
      resume_snippet: "Self-studied AWS services",
      jd_requirement: "Cloud certifications preferred",
      improvement: "Obtain AWS certification to validate skills"
    },
    status: "pending"
  },
  {
    id: 5,
    type: "project_suggestion",
    title: "Add GraphQL API Project",
    original: "REST API projects only",
    suggested: "Build a full-stack application with GraphQL API",
    reason: "Demonstrates GraphQL end-to-end implementation",
    confidence: 0.88,
    evidence: {
      resume_snippet: "REST API development experience",
      jd_requirement: "GraphQL implementation experience",
      improvement: "Create GraphQL API project with React frontend"
    },
    status: "pending"
  }
]

const getStatusBadge = (status: string) => {
  const variants = {
    pending: { variant: "secondary" as const, text: "Pending" },
    accepted: { variant: "default" as const, text: "Accepted" },
    rejected: { variant: "destructive" as const, text: "Rejected" },
    applied: { variant: "default" as const, text: "Applied" }
  }
  return variants[status as keyof typeof variants] || variants.pending
}

const getConfidenceColor = (confidence: number) => {
  if (confidence >= 0.8) return "text-green-600"
  if (confidence >= 0.6) return "text-yellow-600"
  return "text-red-600"
}

const getSuggestionIcon = (type: string) => {
  const icons = {
    skill_highlight: Edit3,
    experience_reword: Edit3,
    skill_addition: Plus,
    certification_suggestion: CheckCircle,
    project_suggestion: Lightbulb
  }
  return icons[type as keyof typeof icons] || Edit3
}

export default function TailoringPage() {
  const [suggestions, setSuggestions] = useState(tailoringSuggestions)
  const [selectedSuggestion, setSelectedSuggestion] = useState<number | null>(null)
  const [customFeedback, setCustomFeedback] = useState('')
  const [isGenerating, setIsGenerating] = useState(false)

  const handleSuggestionAction = (suggestionId: number, action: 'accept' | 'reject') => {
    setSuggestions(prev => 
      prev.map(suggestion => 
        suggestion.id === suggestionId 
          ? { ...suggestion, status: action }
          : suggestion
      )
    )
  }

  const handleEditSuggestion = (suggestionId: number, field: string, value: string) => {
    setSuggestions(prev => 
      prev.map(suggestion => 
        suggestion.id === suggestionId 
          ? { ...suggestion, [field]: value }
          : suggestion
      )
    )
  }

  const generateMoreSuggestions = async () => {
    setIsGenerating(true)
    // Mock generation process
    setTimeout(() => {
      const newSuggestion = {
        id: suggestions.length + 1,
        type: "skill_addition",
        title: "Add Testing Framework Experience",
        original: "Manual testing processes",
        suggested: "Experience with Jest and React Testing Library",
        reason: "Automated testing is industry standard",
        confidence: 0.75,
        evidence: {
          resume_snippet: "Manual testing approaches",
          jd_requirement: "Testing framework experience",
          improvement: "Add automated testing to projects"
        },
        status: "pending"
      }
      setSuggestions(prev => [...prev, newSuggestion])
      setIsGenerating(false)
    }, 2000)
  }

  const applyAllAccepted = () => {
    const acceptedSuggestions = suggestions.filter(s => s.status === 'accepted')
    if (acceptedSuggestions.length === 0) {
      alert('Please accept at least one suggestion to apply')
      return
    }
    // Mock application process
    alert(`Applying ${acceptedSuggestions.length} suggestions to your resume...`)
  }

  const exportSuggestions = () => {
    const dataStr = JSON.stringify(suggestions, null, 2)
    const blob = new Blob([dataStr], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'tailoring-suggestions.json'
    a.click()
    URL.revokeObjectURL(url)
  }

  return (
    <AppLayout>
      <div className="max-w-6xl mx-auto space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold tracking-tight">Tailoring Review</h1>
            <p className="text-muted-foreground">
              Review and customize AI-generated suggestions to improve your resume
            </p>
          </div>
          <div className="flex space-x-2">
            <Button variant="outline" onClick={generateMoreSuggestions} disabled={isGenerating}>
              {isGenerating ? (
                <>
                  <RefreshCw className="mr-2 h-4 w-4 animate-spin" />
                  Generating...
                </>
              ) : (
                <>
                  <RefreshCw className="mr-2 h-4 w-4" />
                  Generate More
                </>
              )}
            </Button>
            <Button variant="outline" onClick={exportSuggestions}>
              <Download className="mr-2 h-4 w-4" />
              Export
            </Button>
          </div>
        </div>

        {/* Summary Stats */}
        <div className="grid gap-4 md:grid-cols-4">
          <Card>
            <CardContent className="pt-6">
              <div className="text-center">
                <div className="text-2xl font-bold text-primary">
                  {suggestions.length}
                </div>
                <p className="text-sm text-muted-foreground">
                  Total Suggestions
                </p>
              </div>
            </CardContent>
          </Card>
          
          <Card>
            <CardContent className="pt-6">
              <div className="text-center">
                <div className="text-2xl font-bold text-green-600">
                  {suggestions.filter(s => s.status === 'accepted').length}
                </div>
                <p className="text-sm text-muted-foreground">
                  Accepted
                </p>
              </div>
            </CardContent>
          </Card>
          
          <Card>
            <CardContent className="pt-6">
              <div className="text-center">
                <div className="text-2xl font-bold text-yellow-600">
                  {suggestions.filter(s => s.status === 'pending').length}
                </div>
                <p className="text-sm text-muted-foreground">
                  Pending Review
                </p>
              </div>
            </CardContent>
          </Card>
          
          <Card>
            <CardContent className="pt-6">
              <div className="text-center">
                <div className="text-2xl font-bold text-red-600">
                  {Math.round(suggestions.reduce((acc, s) => acc + s.confidence, 0) / suggestions.length * 100)}%
                </div>
                <p className="text-sm text-muted-foreground">
                  Avg. Confidence
                </p>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Suggestions List */}
        <div className="space-y-4">
          {suggestions.map((suggestion) => {
            const statusBadge = getStatusBadge(suggestion.status)
            const Icon = getSuggestionIcon(suggestion.type)
            const confidenceColor = getConfidenceColor(suggestion.confidence)
            
            return (
              <Card key={suggestion.id} className="transition-all duration-200">
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div className="flex items-center space-x-3">
                      <Icon className="h-5 w-5 text-primary" />
                      <div>
                        <CardTitle className="text-lg">{suggestion.title}</CardTitle>
                        <Badge variant={statusBadge.variant} className="ml-2">
                          {statusBadge.text}
                        </Badge>
                      </div>
                    </div>
                    <div className="flex items-center space-x-2">
                      <div className="text-right">
                        <div className={`text-sm font-medium ${confidenceColor}`}>
                          {Math.round(suggestion.confidence * 100)}%
                        </div>
                        <div className="text-xs text-muted-foreground">Confidence</div>
                      </div>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => setSelectedSuggestion(
                          selectedSuggestion === suggestion.id ? null : suggestion.id
                        )}
                      >
                        <Eye className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                  <CardDescription className="mt-2">
                    {suggestion.reason}
                  </CardDescription>
                </CardHeader>
                
                {selectedSuggestion === suggestion.id && (
                  <CardContent className="border-t">
                    <div className="space-y-4">
                      {/* Evidence Section */}
                      <div>
                        <h4 className="font-medium mb-2 flex items-center">
                          <AlertCircle className="mr-2 h-4 w-4" />
                          Evidence & Analysis
                        </h4>
                        <div className="bg-muted/30 p-3 rounded-lg space-y-2">
                          <div>
                            <span className="text-sm font-medium">Resume Snippet:</span>
                            <p className="text-sm text-muted-foreground mt-1">
                              "{suggestion.evidence.resume_snippet}"
                            </p>
                          </div>
                          <div>
                            <span className="text-sm font-medium">JD Requirement:</span>
                            <p className="text-sm text-muted-foreground mt-1">
                              "{suggestion.evidence.jd_requirement}"
                            </p>
                          </div>
                          <div>
                            <span className="text-sm font-medium">Improvement:</span>
                            <p className="text-sm text-muted-foreground mt-1">
                              {suggestion.evidence.improvement}
                            </p>
                          </div>
                        </div>
                      </div>

                      {/* Edit Section */}
                      <div>
                        <h4 className="font-medium mb-2">Customize Suggestion</h4>
                        <div className="space-y-3">
                          <div>
                            <label className="block text-sm font-medium mb-1">Suggested Change</label>
                            <Textarea
                              value={suggestion.suggested}
                              onChange={(e) => handleEditSuggestion(suggestion.id, 'suggested', e.target.value)}
                              className="min-h-[80px]"
                            />
                          </div>
                          <div>
                            <label className="block text-sm font-medium mb-1">Add Feedback</label>
                            <Textarea
                              value={customFeedback}
                              onChange={(e) => setCustomFeedback(e.target.value)}
                              placeholder="Add any additional feedback or notes..."
                              className="min-h-[60px]"
                            />
                          </div>
                        </div>
                      </div>
                    </div>
                  </CardContent>
                )}

                <CardContent className="pt-4">
                  <div className="flex items-center justify-between">
                    <div className="flex space-x-2">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => handleSuggestionAction(suggestion.id, 'reject')}
                        disabled={suggestion.status === 'applied'}
                      >
                        <X className="mr-2 h-4 w-4" />
                        Reject
                      </Button>
                      <Button
                        size="sm"
                        onClick={() => handleSuggestionAction(suggestion.id, 'accept')}
                        disabled={suggestion.status === 'applied'}
                      >
                        <CheckCircle className="mr-2 h-4 w-4" />
                        Accept
                      </Button>
                    </div>
                    <Badge variant={suggestion.status === 'applied' ? 'default' : 'secondary'}>
                      {suggestion.status === 'applied' ? 'Applied' : 'Not Applied'}
                    </Badge>
                  </div>
                </CardContent>
              </Card>
            )
          })}
        </div>

        {/* Action Buttons */}
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <div>
                <h4 className="font-medium">Apply Changes</h4>
                <p className="text-sm text-muted-foreground">
                  Apply all accepted suggestions to your resume
                </p>
              </div>
              <Button onClick={applyAllAccepted}>
                <CheckCircle className="mr-2 h-4 w-4" />
                Apply {suggestions.filter(s => s.status === 'accepted').length} Changes
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </AppLayout>
  )
}
